#include <string>
#include <ctime>
#include <cstdio>

int main()
{
  int sec_in_week = 7 * 24 * 60 * 60 ; // for going back one week

  // int now = time(0);
  int now = 1500552000; // assuming no earlier then 07/20/2017 @ 12:00pm (UTC)


  for (size_t seed = now ; seed > now - sec_in_week; seed--) {
    srand(seed);
    printf("\n%d ",seed);
    for (size_t i = 0; i < 32; i++) { // generate 32 random numbers with given seed
      int s=rand();
      printf("%d ", s);
    }
  }

}
