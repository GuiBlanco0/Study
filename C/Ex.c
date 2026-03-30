#include <stdio.h>

int main()
{
    int num = 0;
    printf("Digite o número desejado: ");
    scanf("%d", &num);

    for (int i = 0; i <= 10; i++){

        printf("%d x %d = %d\n", i, num, i*num);
    }
    return 0;
}
