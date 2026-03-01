#include <stdio.h> 
//Adding a Function for Linear Search
int buscaLinear(int arr[], int n, int key) { 
    for (int i = 0; i < n; i++) { 
        if (arr[i] == key) 
            return i; 
    } 
    // If the key is not found in the array, return -1 (Non existent in the array)
    return -1; 
}
//Actual Main Function
int main(){
    int alunos;
    int notas[50];
    char nomes[50][50]; // Array of strings needs a "char" type and two dimensions
    int Nota_Procurada;
    printf("Digite a quantidade de Alunos: ");
    scanf("%d", &alunos);
    for(int i = 0; i < alunos; i++){
        printf("Digite o nome do aluno %d: ", i + 1);
        scanf("%s", nomes[i]);
        printf("Digite a nota do aluno %d: ", i + 1);
        scanf("%d", &notas[i]);
    }
    printf("Digite a nota que deseja buscar: ");
    scanf("%d", &Nota_Procurada);  
    // Calling the Linear Search Function
    int pos = buscaLinear(notas, alunos, Nota_Procurada);
    if (pos == -1) {
        printf("Nota nao encontrada.\n");
    } else {
        printf("Nota encontrada na posicao: %d\n", pos + 1);
        printf("Nome do aluno: %s\n", nomes[pos]);
    }
    return 0;
}   