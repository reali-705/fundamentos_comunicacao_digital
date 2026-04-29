import numpy as np
import matplotlib.pyplot as plt


# Define a função periódica original que será aproximada pela série de Fourier.
# A função é dada por seno de t mais meio cosseno de 2t.
def minha_funcao(t):
    return np.sign(np.sin(t))

# Calcula os coeficientes an e bn da série de Fourier para o harmônico n.
# A integração é feita numericamente usando soma de Riemann com num_passos passos.
def calcular_coeficiente(n, omega0, T):
    soma_a = 0
    soma_b = 0
    num_passos = 1000
    dt = T / num_passos
    for i in range(num_passos):
        t = i * dt
        soma_a += minha_funcao(t) * np.cos(n * omega0 * t) * dt
        soma_b += minha_funcao(t) * np.sin(n * omega0 * t) * dt

    # Normaliza a soma para obter o coeficiente correto da série.
    return (2/T * soma_a, 2/T * soma_b)

# Reconstrói o sinal em um ponto t_alvo usando até max_harmonicos harmônicos.
def reconstruir_sinal(t_alvo, max_harmonicos, T):
    omega0 = 2 * np.pi / T

    # a0 é o coeficiente do termo constante da série de Fourier.
    a0, _ = calcular_coeficiente(0, omega0, T)
    resultado = a0 / 2

    # Soma os termos harmônicos de 1 até max_harmonicos.
    for n in range(1, max_harmonicos + 1):
        an, bn = calcular_coeficiente(n, omega0, T)
        resultado += (
            an * np.cos(n * omega0 * t_alvo) +
            bn * np.sin(n * omega0 * t_alvo)
        )
    return resultado

# Função principal que gera o gráfico do sinal original e de sua reconstrução.
def main():
    T = 2 * np.pi  # Período da função original.
    max_harmonicos = 1 # Número de harmônicos a serem usados na reconstrução.

    # Ponto de análise e vetor de tempo para plotagem.
    t_valores = np.linspace(0, T, 1000) # Gera 1000 pontos entre 0 e T para uma representação suave do sinal.
    y_original = minha_funcao(t_valores)

    # Reconstrói o sinal para cada ponto de t_valores.
    y_reconstruida = np.array([
        reconstruir_sinal(t, max_harmonicos, T)
        for t in t_valores
    ])

    # Plota o sinal original e o sinal reconstruído usando a série de Fourier.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    ax1.plot(t_valores, y_original, label='Sinal Original', color='blue')
    ax1.set_title('Sinal Original')
    ax1.set_xlabel('Tempo (t)')
    ax1.set_ylabel('f(t)')
    ax1.grid(True, alpha=0.3)

    ax2.plot(t_valores, y_reconstruida, linestyle="--", color="tomato")
    ax2.set_title(f"Reconstruído ({max_harmonicos} harmônicos)")
    ax2.set_xlabel("t")
    ax2.set_ylabel("f(t)")
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Série de Fourier", fontsize=14)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()