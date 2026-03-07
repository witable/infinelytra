#include <pybind11/pybind11.h>
#include <random>
#include <pybind11/stl.h> // Allows passing lists/vectors
#include <array>
#include <math.h>

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
    array<double, 3> arr{{k * l, -m, j * l}};
    return arr;
}

array<double, 3> run_physics(double& vx, double& vy, double& vz, const double& x, const double& y)
{   
    array<double, 3> v2 = (calculateViewVector(x,y));
    const double f = x * PI / 180;
    const double d = sqrt(v2[0]*v2[0] + v2[2]*v2[2]);
    const double e = sqrt(vx*vx + vz*vz);
    const double g = 0.08;
    const double h = cos(f) * cos(f);
    vy += g * (-1 + h * 0.75);

    if (vy < 0 and d > 0)
    {
        const double i = vy * -0.1 * h;
        vx += v2[0] * i / d;
        vy += i;
        vz += v2[2] * i / d;

    }
        
    if (f < 0 and d > 0)
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
    array<double, 3> arr{{vx * 0.99, vy * 0.98, vz * 0.99}};
    return arr;
}


double update_physics(double positionY, vector<double> gene, int maxTick)
{
    double positionx = 0;
    double positiony = positionY;
    double positionz = 0;
    double currentPitch = 0;
    array<double, 3> movement{{0,0,0}};
    
    for (int i = 0; i < maxTick; i++)
    {
        currentPitch = currentPitch+gene[i];
        //if (positiony > 0)
        //{
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
        //}
    }        
    return sqrt(positionx*positionx + positionz*positionz);

}

vector<double> mutate(vector<double> gene, double mutation_rate) 
{
    int n = gene.size();
    static std::random_device rd;
    static std::mt19937 gen(rd());
    
    std::uniform_real_distribution<double> chance(0.0, 1.0);
    std::uniform_real_distribution<double> delta(-1.0, 1.0);

    for (int i = 0; i < n; i++) 
    {
        if (chance(gen) < mutation_rate) 
        {
            gene[i] += delta(gen);
            if (gene[i] > 1.0) {
                gene[i] = 1.0;
            }
            if (gene[i] < -1.0) {
                gene[i] = -1.0;
            }
        }
    }
    return gene;
}

array<vector<double>, 2> crossover(vector<double> geneA, vector<double> geneB) 
{
    int n = geneA.size();
    static std::random_device rd;
    static std::mt19937 gen(rd());
    
    std::uniform_int_distribution<int> dist(0, n-1);
    vector<double> geneAOut(n);
    vector<double> geneBOut(n);
    int p = dist(gen);
    for (int i = 0; i < p; i++) 
    {
        geneAOut[i] = geneA[i];
        geneBOut[i] = geneB[i];
    }
    for (int i = p; i < n; i++) 
    {
        geneAOut[i] = geneB[i];
        geneBOut[i] = geneA[i];
    }
    array<vector<double>, 2> arr{{geneAOut,geneBOut}};
    return arr;
}



PYBIND11_MODULE(elytra_physics, m) {
    m.def("update_physics", &update_physics, "A function to update elytra movement");
    m.def("mutate", &mutate, "A function to mutate genes");
    m.def("crossover", &crossover, "A function to crossover genes");
}