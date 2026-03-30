#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    printf("Guess Game!\n");
    int segundos = time(0);
    srand(segundos);
    int bigNumber = rand();
    int secretnumber = bigNumber % 100;
    int guess;
    int number_of_tries = 1;
    double points = 1000;

    while(1) { // Infinite loop, will break only when theres a break statement
        printf("Tentativa %d\n", number_of_tries);
        printf("Qual o seu chute? ");
        scanf("%d", &guess);

        //validate the guess
        if (guess < 0 || guess > 100) {
            printf("Chute invalido! Por favor, chute um numero entre 0 e 100.\n");
            continue; // Jump to the next iteration of the loop

        } else if(guess == secretnumber) {
            printf("Parabens, voce acertou!\n");
            break;
        }
        else{
            if(guess > secretnumber){
                printf("Seu chute foi maior que o numero secreto\n");
            }
            else{
                printf("Seu chute foi menor que o numero secreto\n");
            }
        }
        number_of_tries++;
        double lostPoints = (guess - secretnumber) / 2.0;
        //Modifying Alura's class code
        if (lostPoints < 0){
            lostPoints = lostPoints * -1;
        }
        else{
            lostPoints = lostPoints;
        }
        points = points - lostPoints;
    }
    printf("Fim de jogo!");
    printf("Voce acertou em %d tentativas!\n", number_of_tries);
    printf("Total de pontos: %.1f\n", points);

    return 0;
}
