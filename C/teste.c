#include <stdio.h>

int main() {
    char nome[50];
    int idade;

    printf("Digite seu nome: ");
    scanf("%s", nome);

    printf("Digite sua idade: ");
    scanf("%d", &idade);

    printf("\nOla %s! Voce tem %d anos.\n", nome, idade);
    printf("Daqui a 5 anos voce tera %d anos.\n", idade + 5);

    return 0;
}