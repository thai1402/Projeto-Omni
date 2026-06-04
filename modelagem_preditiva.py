import pandas as pd

df = pd.read_excel("Base_Integrada.xlsx")

print(df.head())
df["Alvo"] = (
    df["Compra_Finalizada"]
    .str.upper()
    .eq("SIM")
    .astype(int)
)
frequencia = (
    df.groupby("Nome")
    .size()
    .reset_index(name="Frequencia_Acesso")
)
ticket = (
    df.groupby("Nome")["Total_Gasto"]
    .mean()
    .reset_index(name="Ticket_Medio")
)
df["Data_Compra"] = (
    df["Data_Compra"]
    .astype(str)
    .str.strip()
)

df["Data_Compra"] = pd.to_datetime(
    df["Data_Compra"],
    errors="coerce"
)
ultima_data = df["Data_Compra"].max()

recencia = (
    df.groupby("Nome")["Data_Compra"]
    .max()
    .reset_index()
)

recencia["Recencia"] = (
    ultima_data - recencia["Data_Compra"]
).dt.days
categoria = (
    df.groupby("Nome")["Categoria"]
    .agg(lambda x: x.mode()[0])
    .reset_index(name="Categoria_Preferida")
)
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

categoria["Categoria_Preferida"] = le.fit_transform(
    categoria["Categoria_Preferida"]
)
base_ml = frequencia.merge(ticket, on="Nome")
base_ml = base_ml.merge(
    recencia[["Nome", "Recencia"]],
    on="Nome"
)
base_ml = base_ml.merge(
    categoria,
    on="Nome"
)

alvo = (
    df.groupby("Nome")["Alvo"]
    .max()
    .reset_index()
)

base_ml = base_ml.merge(alvo, on="Nome")