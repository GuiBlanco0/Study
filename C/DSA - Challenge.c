#include <stdio.h> 
//Adding a Function for Linear Search
int buscaLinear(int arr[], int n, int key) { 
    for (int i = 0; i < n; i++) { 
        if (arr[i] == key) 
            return i; 
    } 
    return -1; 
}
//Actual Main Function
int main(){
    int alunos;
    int notas[50];
    int Nota_Procurada;
    printf("Digite a quantidade de Alunos: ");
    scanf("%d", &alunos);
    for(int i = 0; i < alunos; i++){
        printf("Digite a nota do aluno %d: ", i + 1);
        scanf("%d", &notas[i]);
    }
    printf("Digite a nota que deseja buscar: ");
    scanf("%d", &Nota_Procurada);  
    int pos = buscaLinear(notas, alunos, Nota_Procurada);
    if (pos == -1) {
        printf("Nota nao encontrada.\n");
    } else {
        printf("Nota encontrada na posicao: %d\n", pos + 1);
    }
    return 0;
}   