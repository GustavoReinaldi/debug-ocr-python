from PrettyColorPrinter import add_printer
from pdferli import get_pdfdf
import numpy as np
import pandas as pd

path = "./files/modelo_de_nota_de_envio_de_amostra.pdf"
add_printer(1)
# DataFrame do Pandas com todos os dados extraídos das imagens
df = get_pdfdf(path, normalize_content=False)
togi = []
# Ele faz a "paginação" do DataFrame, separando através das linhas LTAnno
for r in np.split(df, df.loc[df.aa_element_type == "LTAnno"].index):   
    # Remove as linhas que não possuem o tamanho do texto pela coluna aa_size (Linhas do LTAnno - Que é uma quebra de linha)
    df2 = r.dropna(subset="aa_size")
    # Se o DataFrame não estiver vazio ele cria um 3º DataFrame ordenando pela coluna aa_x0
    if not df2.empty:
        # Ordena do menor para o maior        
        df3 = df2.sort_values(by="aa_x0")
        # Pega a primeira linha dessa pagina do DataFrame
        togi.append(df3.iloc[:1].copy())
df4 = pd.concat(togi).copy()
df4.loc[:, "x0round"] = df4.aa_x0.round(2)
resultado = []
for name, group in df4.groupby("x0round"):
    if len(group) > 1:
        group2 = group.reset_index(drop=True)
        group3 = np.split(
            group2, group2.loc[group2.aa_fontname == "Helvetica-Bold"].index
        )
        for group4 in group3:
            if len(group4) > 1:
                group5 = group4.sort_values(by="bb_hierachy_page")
                t1 = group5.aa_text_line.iloc[0]
                t2 = "\n".join(group5.aa_text_line.iloc[1:].to_list())
                resultado.append((t1, t2))

df5 = pd.DataFrame(resultado).set_index(0).T.to_html("files/export.html", index=False)
