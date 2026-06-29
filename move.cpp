#include <pybind11/pybind11.h>
#include <random>
#include <pybind11/numpy.h>
#include <array>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>

#define PI 3.14159265
namespace py = pybind11;
using namespace std;

array<double, 3> calculateViewVector(const double& x, const double& y)
{
    const double h = x * PI / 180;
    const double i = -y * PI / 180;
    const double j = cos(i);
    const double k = sin(i);
    const double l = cos(h);
    const double m = sin(h);
    return {{k * l, -m, j * l}};
}

array<double, 3> run_physics(double& vx, double& vy, double& vz, const double& x, const double& y)
{   
    array<double, 3> v2 = calculateViewVector(x,y);
    const double f = x * PI / 180;
    const double d = sqrt(v2[0]*v2[0] + v2[2]*v2[2]);
    const double e = sqrt(vx*vx + vz*vz);
    const double g = 0.08;
    const double h = cos(f) * cos(f);
    vy += g * (-1 + h * 0.75);

    if (vy < 0 && d > 0)
    {
        const double i = vy * -0.1 * h;
        vx += v2[0] * i / d;
        vy += i;
        vz += v2[2] * i / d;
    }
        
    if (f < 0 && d > 0)
    {
        const double i = e * -sin(f) * 0.04;
        vx += -v2[0] * i / d;
        vy += i * 3.2;
        vz += -v2[2] * i / d;
    }

    if (d > 0)
    {
        vx += (v2[0] / d * e - vx) * 0.1;
        vz += (v2[2] / d * e - vz) * 0.1;
    }
    return {{vx * 0.99, vy * 0.98, vz * 0.99}};
}

py::tuple next_physics(double& vx, double& vy, double& vz, const double& xPitch, const double& yPitch, double x, double y, double z)
{   
    array<double, 3> v2 = calculateViewVector(xPitch,yPitch);
    const double f = xPitch * PI / 180;
    const double d = sqrt(v2[0]*v2[0] + v2[2]*v2[2]);
    const double e = sqrt(vx*vx + vz*vz);
    const double g = 0.08;
    const double h = cos(f) * cos(f);
    vy += g * (-1 + h * 0.75);

    if (vy < 0 && d > 0)
    {
        const double i = vy * -0.1 * h;
        vx += v2[0] * i / d;
        vy += i;
        vz += v2[2] * i / d;
    }
        
    if (f < 0 && d > 0)
    {
        const double i = e * -sin(f) * 0.04;
        vx += -v2[0] * i / d;
        vy += i * 3.2;
        vz += -v2[2] * i / d;
    }

    if (d > 0)
    {
        vx += (v2[0] / d * e - vx) * 0.1;
        vz += (v2[2] / d * e - vz) * 0.1;
    }
    vx *= 0.99;
    vy *= 0.98;
    vz *= 0.99;

    x += vx;
    y += vy;
    z += vz;

    return py::make_tuple(x, y, z, vx, vy, vz);
}

double check_physics(int maxTick, double positionY)
{
    std::ifstream file("out.txt");
    double value;
    vector<double> pitchX;

    if (file.is_open()) {
        while (file >> value) { // Reads one double at a time
            pitchX.push_back(value);
        }
        file.close();
    }
    
    double positionx = 0;
    double positiony = positionY;
    double positionz = 0;
    array<double, 3> movement{{0,0,0}};
    double currentPitch = 0;
    
    for (int i = 0; i < maxTick; i++)
    {
        currentPitch += pitchX[i];
        if (positiony > 0)
        {

            if (currentPitch > 90)
            {
                currentPitch = 90;
            }
            if (currentPitch < -90)
            {
                currentPitch = -90;
            }
            
            movement = run_physics(movement[0], movement[1], movement[2], currentPitch, 0);
            
            positionx += movement[0];
            positiony += movement[1];
            positionz += movement[2];
        }
    }        
    return sqrt(positionx*positionx + positionz*positionz);
}

double update_physics(double positionY, py::array_t<double> gene_array, int maxTick)
{
    double positionx = 0;
    double positiony = positionY;
    double positionz = 0;
    double currentPitch = 0;
    array<double, 3> movement{{0,0,0}};
    
    auto gene = gene_array.unchecked<1>();
    for (int i = 0; i < maxTick; i++)
    {
        currentPitch = currentPitch + gene(i);
        if (positiony > 0)
        {

            if (currentPitch > 90)
            {
                currentPitch = 90;
            }
            if (currentPitch < -90)
            {
                currentPitch = -90;
            }
            movement = run_physics(movement[0], movement[1], movement[2], currentPitch, 0);
            
            positionx += movement[0];
            positiony += movement[1];
            positionz += movement[2];
        }
    }        
    return sqrt(positionx*positionx + positionz*positionz);
}

py::array_t<double> mutate(py::array_t<double> gene_array, double mutation_rate) 
{
    auto gene = gene_array.unchecked<1>();
    int n = gene.shape(0);

    auto result = py::array_t<double>(n);
    auto result_buf = result.mutable_unchecked<1>();
    
    static std::random_device rd;
    static std::mt19937 gen(rd());
    
    std::uniform_real_distribution<double> chance(0.0, 1.0);
    std::uniform_real_distribution<double> delta(-1.0, 1.0);

    for (int i = 0; i < n; i++) 
    {
        result_buf(i) = gene(i);
        if (chance(gen) < mutation_rate) 
        {
            result_buf(i) += delta(gen);
            if (result_buf(i) > 3.0) result_buf(i) = 3.0;
            if (result_buf(i) < -3.0) result_buf(i) = -3.0;
        }
    }
    return result;
}

py::tuple crossover(py::array_t<double> geneA_array, py::array_t<double> geneB_array) 
{
    auto geneA = geneA_array.unchecked<1>();
    auto geneB = geneB_array.unchecked<1>();
    int n = geneA.shape(0);
    
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(0, n-1);
    
    auto resultA = py::array_t<double>(n);
    auto resultB = py::array_t<double>(n);
    auto bufA = resultA.mutable_unchecked<1>();
    auto bufB = resultB.mutable_unchecked<1>();
    
    int p = dist(gen);
    
    for (int i = 0; i < p; i++) 
    {
        bufA(i) = geneA(i);
        bufB(i) = geneB(i);
    }
    for (int i = p; i < n; i++) 
    {
        bufA(i) = geneB(i);
        bufB(i) = geneA(i);
    }
    
    return py::make_tuple(resultA, resultB);
}

PYBIND11_MODULE(elytra_physics, m) {
    m.def("check_physics", &check_physics, "Yes");
    m.def("next_physics", &next_physics, "Next pos");
    m.def("update_physics", &update_physics, "A function to update elytra movement");
    m.def("mutate", &mutate, "A function to mutate genes");
    m.def("crossover", &crossover, "A function to crossover genes");
}