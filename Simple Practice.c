#include <stdio.h>
#include <math.h>

int main() {
    int A, B, C;
    float delta, resultPos, resultNeg;
    printf("Digite o valor de A: ");
    scanf("%d", &A);
    printf("Digite o valor de B: ");
    scanf("%d", &B);
    printf("Digite o value de C: ");
    scanf("%d", &C);
    if (A == 0) {
        printf("Se A e zero, nao e uma equacao do segundo grau!\n");
        return 1;
    }
    delta = (B * B) - (4 * A * C);
    if (delta < 0) {
        printf("Delta e %.1f. A equacao nao possui raizes reais.\n", delta);
    } else {
        resultPos = (-B + sqrt(delta)) / (2 * (float)A);
        resultNeg = (-B - sqrt(delta)) / (2 * (float)A);
        printf("As raizes sao: %.2f e %.2f\n", resultPos, resultNeg);
    }

    return 0;
}