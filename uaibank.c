#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char nome[100];
    int idade;
    double saldo;
} Usuario;

Usuario *usuario;

int total_users = 0;
int id = 0;
int usuarios_excluidos[100];
int id_excluido=-1;
int quantidade_de_exclusoes=-1;
int capacidade_maxima=0;

void alocar_usuario()
{
    if(total_users==0)
    {
        capacidade_maxima = 50;
        usuario = (Usuario*)malloc(capacidade_maxima*sizeof(Usuario));
        if(usuario==NULL)
        {
            printf("Nao foi possivel alocar a memoria dinamicamente");
            exit(EXIT_FAILURE);
        }
    }
    else if(total_users>=capacidade_maxima)
    {
        capacidade_maxima +=50;
        Usuario *temp = (Usuario*)realloc(usuario, capacidade_maxima*sizeof(Usuario));
        if(temp==NULL)
        {
            printf("Erro ao realocar a memoria");
            free(usuario);
            exit(EXIT_FAILURE);
        }
        usuario = temp;
    }
}
void criar_usuario()
{
    char nome2[100];
    printf("\nDigite seu nome, idade e saldo atual: ");
    scanf("%100[^,], %d, %lf", usuario[total_users].nome, &usuario[total_users].idade, &usuario[total_users].saldo);
    total_users++;
    printf("Usuario inserido com id %d\n", total_users - 1);
}

void salva_usuarios()
{
    FILE *f;
    f = fopen("usuarios.txt", "w");
    if (f == NULL) {
        printf("Erro ao abrir arquivo para escrita.\n");
        return;
    }
    for (int i = 0; i < total_users; i++) {
        fprintf(f, "%s, %d, %.2lf\n", usuario[i].nome, usuario[i].idade, usuario[i].saldo);
        id++;
    }
    fclose(f);
}

void carrega_usuarios()
{
    FILE *f;
    f = fopen("usuarios.txt", "r");
    if (f == NULL) {
        printf("Arquivo de usuarios nao encontrado. Nenhum usuario carregado.\n");
        return;
    }
    total_users = 0;
    capacidade_maxima = 0;
    if (usuario != NULL) {
        free(usuario);
        usuario = NULL;
    }
    Usuario temp_user;
    while (fscanf(f, " %99[^,], %d, %lf\n", temp_user.nome, &temp_user.idade, &temp_user.saldo) == 3) {
        alocar_usuario();
        strcpy(usuario[total_users].nome, temp_user.nome);
        usuario[total_users].idade = temp_user.idade;
        usuario[total_users].saldo = temp_user.saldo;
        total_users++;
    }
    fclose(f);
}

void buscar_id()
{
    int controle=0;
    printf("Digite o id que deseja acessar: ");
    scanf("%d", &id);
    if (id >= 0 && id < total_users) {
        if(strcmp(usuario[id].nome,"Usuario removido")==0 && usuario[id].idade==-1 && usuario[id].saldo==-1)
            printf("Erro: usuario removido\n");
        else
            printf("Usuario de id %d: \n%s, %d, %.2lf\n", id, usuario[id].nome, usuario[id].idade, usuario[id].saldo);
    }
    else
        {
        printf("Usuario nao encontrado\n");
        }
}

void criar_varios_usuarios()
{
    int n = 0;
    printf("Digite quantos usuarios voce quer cadastrar:");
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        printf("\nDigite seu nome, idade e saldo atual: ");
        scanf("%100[^,], %d, %lf", usuario[total_users].nome, &usuario[total_users].idade, &usuario[total_users].saldo);
        total_users++;
        printf("O id do usuario criado e: %d\n", total_users - 1);
        salva_usuarios();
    }
}

void transferencia()
{
    int valor = 0, id1, id2;
    printf("Digite o id do usuario que vai transferir:");
    scanf("%d", &id);
    id1 = id;
    if(strcmp(usuario[id1].nome,"Usuario removido")==0 || id1<0 || id1>total_users-1)
    {
        printf("Erro: usuario removido ou inexistente\n");
        return;
    }
    printf("Digite o valor a ser transferido:");
    scanf("%d", &valor);
    if (valor > usuario[id1].saldo || valor < 0) {
        printf("Erro. Valor indisponivel.\n");
        return;
    } else {
        printf("Digite o id do usuario que vai receber a transferencia:");
        scanf("%d", &id);
        id2 = id;
        if(id2 == id1)
        {
            printf("Erro: transferencia propria\n");
            return;
        }
        else if(strcmp(usuario[id].nome,"Usuario removido")==0 || id2<0 || id2>total_users-1)
        {
            printf("Erro: usuario removido ou inexistente\n");
            return;
        }
        usuario[id1].saldo = usuario[id1].saldo - valor;
        salva_usuarios();
        usuario[id2].saldo = usuario[id2].saldo + valor;
        salva_usuarios();
        printf("Transferencia realizada com sucesso!\n");
    }
}

void excluir()
{
    printf("Digite o id que voce deseja excluir:");
    scanf("%d",&id);
    id_excluido = id;
    if(strcmp(usuario[id_excluido].nome,"Usuario removido")==0 || id_excluido<0 || id_excluido>total_users-1)
    {
        printf("Erro: usuario removido ou inexistente\n");
        return;
    }
    usuarios_excluidos[++quantidade_de_exclusoes] = id_excluido;
    strcpy(usuario[id_excluido].nome, "Usuario removido");
    salva_usuarios();
    usuario[id_excluido].idade = -1;
    salva_usuarios();
    usuario[id_excluido].saldo = -1;
    salva_usuarios();
    printf("Usuario removido com sucesso\n");
}

int main()
{
    alocar_usuario();
    carrega_usuarios();
    int sele;
    printf("||||| <------ MENU ------> |||||\n");
    printf("1- Criar um usuario\n");
    printf("2- Criar varios usuarios\n");
    printf("3- Buscar um usuario por id\n");
    printf("4- Transferir para outro usuario\n");
    printf("5- Remover um usuario\n");
    printf("6- Encerrar sistema\n");
    printf("Escolha uma das opcoes de 1 a 6: ");
    scanf("%d", &sele);
    if (sele > 6 || sele < 1)
        {
        printf("Erro: valor fora dos limites\n");
        main();
        }
    else if (sele == 1)
        {
        alocar_usuario();
        criar_usuario();
        salva_usuarios();
        main();
        }
    else if (sele == 2)
        {
        criar_varios_usuarios();
        main();
        }
    else if (sele == 3)
        {
        buscar_id();
        main();
        }
    else if (sele == 4)
        {
        transferencia();
        main();
        }
    else if (sele == 5)
        {
        excluir();
        main();
        }
    else
        {
        printf("Programa encerrado.");
        free(usuario);
        return 0;
        }
}
