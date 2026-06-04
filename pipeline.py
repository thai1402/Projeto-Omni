import pandas as pd

print("Iniciando processamento...")


clientes = pd.read_excel(
    "Base de Dados 1- Cadastro de Clientes (2).xlsx"
)

acessos = pd.read_excel(
    "Base de Dados 2- Acessos e Compras no Site (2).xlsx"
)

pedidos = pd.read_excel(
    "Base de Dados 3- Detalhes dos Pedidos (2).xlsx"
)

print("Arquivos carregados!")


clientes = clientes.iloc[:, 0].str.split(",", expand=True)

clientes.columns = [
    "ID_Cliente",
    "Nome",
    "Email",
    "Telefone",
    "Data_Nascimento"
]

acessos = acessos.iloc[:, 0].str.split(",", expand=True)

acessos.columns = [
    "ID_Sessao",
    "Nome_Cliente",
    "Horario_Inicio",
    "Horario_Termino",
    "Valor_Carrinho",
    "Compra_Finalizada"
]

pedidos = pedidos.iloc[:, 0].str.split(",", expand=True)

pedidos.columns = [
    "ID_Pedido",
    "ID_Sessao",
    "Produto",
    "Categoria",
    "Quantidade",
    "Preco_Unitario",
    "Data_Compra"
]

print("Colunas ajustadas!")

clientes = clientes.drop_duplicates()
acessos = acessos.drop_duplicates()
pedidos = pedidos.drop_duplicates()

pedidos["Quantidade"] = pd.to_numeric(
    pedidos["Quantidade"],
    errors="coerce"
)

pedidos["Preco_Unitario"] = pd.to_numeric(
    pedidos["Preco_Unitario"],
    errors="coerce"
)

acessos["Valor_Carrinho"] = pd.to_numeric(
    acessos["Valor_Carrinho"],
    errors="coerce"
)

print("Pré-processamento concluído!")


pedidos["Total_Gasto"] = (
    pedidos["Quantidade"]
    * pedidos["Preco_Unitario"]
)

acessos["Conversao"] = (
    acessos["Compra_Finalizada"]
    .str.upper()
    .eq("SIM")
    .astype(int)
)

print("Features criadas!")

df = pedidos.merge(
    acessos,
    on="ID_Sessao",
    how="left"
)

df = df.merge(
    clientes,
    left_on="Nome_Cliente",
    right_on="Nome",
    how="left"
)

print("Bases integradas!")

ticket_medio = df["Total_Gasto"].mean()

print("\nTICKET MÉDIO")
print(ticket_medio)

taxa_conversao = (
    df.groupby("Categoria")["Conversao"]
    .mean()
    * 100
)

print("\nTAXA DE CONVERSÃO (%)")
print(taxa_conversao)

receita_categoria = (
    df.groupby("Categoria")["Total_Gasto"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRECEITA POR CATEGORIA")
print(receita_categoria)

melhores_clientes = (
    df.groupby("Nome")["Total_Gasto"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTOP 10 CLIENTES")
print(melhores_clientes.head(10))

media = df["Total_Gasto"].mean()

outliers = df[
    df["Total_Gasto"] > media * 3
]

print("\nOUTLIERS")
print(outliers)

df.to_excel(
    "Base_Integrada.xlsx",
    index=False
)

print("\nArquivo Base_Integrada.xlsx criado com sucesso!")