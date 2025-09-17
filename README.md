# 🏙️ Dashboard de Análise do Mercado Imobiliário de São Paulo

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red?style=for-the-badge&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-purple?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-green?style=for-the-badge&logo=plotly)

<br>

## 📖 Sobre o Projeto

Este projeto consiste em um dashboard interativo para a análise de dados do mercado imobiliário da cidade de São Paulo. A aplicação foi desenvolvida utilizando **Streamlit** e permite que os usuários explorem visualmente os fatores que influenciam os preços de imóveis, como localização, tamanho, e comodidades.

O objetivo é fornecer uma ferramenta intuitiva para que potenciais compradores, vendedores ou analistas de mercado possam extrair insights valiosos de forma rápida e eficaz.

<br>

> **Nota:** Você pode acessar a aplicação online [**AQUI**]().

<br>

### ✨ Demonstração
![Demonstração do Dashboard](link_para_sua_imagem_ou_gif.gif)

---

## 🚀 Funcionalidades

-   **Filtros Interativos:** Segmentação dos dados por tipo de imóvel, bairro, faixa de preço, área, número de quartos e características adicionais (piscina, mobiliado, etc.).
-   **Análise Geográfica:** Mapa de calor interativo que exibe a concentração e o preço por m² dos imóveis na cidade de São Paulo.
-   **Métricas Dinâmicas:** KPIs que se atualizam em tempo real de acordo com os filtros aplicados.
-   **Visualizações de Dados:** Gráficos detalhados para análise de custo-benefício, impacto de comodidades no preço e distribuição da oferta de imóveis.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido com as seguintes tecnologias:

-   **Python:** Linguagem de programação principal.
-   **Streamlit:** Framework para a construção da aplicação web interativa.
-   **Pandas:** Para manipulação e tratamento dos dados.
-   **Plotly Express:** Para a criação dos gráficos interativos.
-   **Git & GitHub:** Para versionamento de código e hospedagem.

---

## 📊 Fonte dos Dados

Os dados utilizados neste projeto foram obtidos do [**Kaggle**](https://www.kaggle.com/datasets/argonalyst/sao-paulo-real-estate-sale-rent-april-2019). O dataset contém informações detalhadas sobre imóveis, incluindo características, custos e localização geográfica.

---

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para rodar a aplicação na sua máquina:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/andrezktt/streamlit_dashboard_imoveis_sp.git
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd streamlit_dashboard_imoveis_sp
    ```

3.  **Instale o UV (package and project manager):**
    ```bash
    pip install -g uv  # Para Windows
    ```

4.  **Sincronize e Instale as dependencias:**
    ```bash
    uv sync
    ```

5.  **Execute a aplicação Streamlit:**
    ```bash
    uv run streamlit run app.py
    ```

A aplicação estará disponível no seu navegador em `http://localhost:8501`.

---

## 👨‍💻 Autor

Desenvolvido por **André Zicatti**.

-   [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andrezicatti/)
-   [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/andrezktt)