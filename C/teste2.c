#include <stdio.h>

int main() {
    float nota1, nota2, media;

    printf("Digite a primeira nota: ");
    scanf("%f", &nota1);

    printf("Digite a segunda nota: ");
    scanf("%f", &nota2);

    media = (nota1 + nota2) / 2;

    printf("Media final: %.2f\n", media);

    if (media >= 6.0) {
        printf("Aprovado!\n");
    } else {
        printf("Reprovado!\n");
    }

    return 0;
}