#include<stdio.h>
#include<stdlib.h>
#include<string.h>
typedef struct{
    char nome[50];
    int idade;
    double saldo;
}usuario;
typedef struct{
    int quantidade;
    int tamanho;
}lista;
int *cadastros;

void alocar_memoria()
{
    (*cadastros) = (int*)malloc(50*sizeof(int));
    if(cadastros == NULL)
    {
        printf("Memoria insuficiente\n");
        exit(1);
    }
}

void criar_usuário()
{
    printf("Digite seu nome, idade e saldo atual:\n");
    scanf("%100[^','], %d, %lf", &usuario.nome, &usuario.idade, &usuario.saldo);
}

int main()
{
    int sele;
    printf("1- Criar um usuario\n");
    printf("2- Criar varios usuarios\n");
    printf("3- Buscar um usuario por id\n");
    printf("4- Transferir para outro usuario\n");
    printf("5- Remover um usuario\n");
    printf("Escolha uma das opcoes de 1 a 5: ");
    scanf("%d", &sele);
    if(sele>5 || sele<1)
    {
        printf("Erro: valor fora dos limites\n");
        main(sele);
    }
    else if(sele==1)
    {

    }
    else if(sele==2)
    {

    }
    else if(sele==3)
    {

    }
    else if(sele==4)
    {

    }
    else
    {

    }
}
