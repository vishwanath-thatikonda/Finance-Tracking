
import pandas as pd
import matplotlib.pyplot as plt

def plot_expenses(data):
    df = pd.DataFrame(data, columns=['Date', 'Category', 'Description', 'Amount'])
    if df.empty:
        return None
    category_summary = df.groupby('Category')['Amount'].sum()
    fig, ax = plt.subplots()
    category_summary.plot(kind='bar', ax=ax)
    ax.set_title('Expenses by Category')
    ax.set_ylabel('Amount')
    return fig
