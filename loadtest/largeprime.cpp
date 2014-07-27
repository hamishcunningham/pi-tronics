#include <iostream>
using namespace std;

// program to count up from 1, trying to find if the number is prime or not

int main()
{
	long long int theMax = 1;
	unsigned short int prime = 1;

	while (theMax > 0) {
		cout << "Testing " << theMax << "...\n";
		prime = 1;
		for (long long int d = ((theMax+1)/2); d > 1; d--)
		{
			if ((theMax % d) == 0)
			{
				prime = 0;
				break;
			}
		}
		if (prime == 0)
		{
			cout << "  " << theMax << " is not prime!\n";
		}
		else if (prime == 1)
		{
			cout << "  \x1b[1m" << theMax << " is prime!\x1b[0m" << endl;
		}
		theMax++;
	}
}
