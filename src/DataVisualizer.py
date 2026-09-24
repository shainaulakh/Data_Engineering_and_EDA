from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


class DataVisualizer:
    """Generates analytical chart deliverables."""

    @staticmethod
    def plot_salary_by_position_and_year(df: pd.DataFrame):
        """Standard Visualization: Grouped bar chart for average salary by position and year."""
        avg_salary_df = (
            df.groupby(["position", "start_year"])["salary"]
            .mean()
            .reset_index()
        )

        plt.figure(figsize=(14, 7))
        sns.barplot(
            data=avg_salary_df,
            x="position",
            y="salary",
            hue="start_year",
            palette="viridis"
        )

        plt.title("Average Salary by Position and Start Year (2015–2024)", fontsize=15, fontweight="bold", pad=15)
        plt.xlabel("IT Position", fontsize=12, labelpad=10)
        plt.ylabel("Average Salary ($)", fontsize=12, labelpad=10)
        plt.xticks(rotation=40, ha="right", fontsize=10)
        plt.legend(title="Start Year", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_department_salary_heatmap(joined_df: pd.DataFrame):
        """Advanced Visualization: Heatmap of mean salary by department and position."""
        pivot_df = joined_df.pivot_table(
            index="dept_name",
            columns="position",
            values="salary",
            aggfunc="mean"
        )

        plt.figure(figsize=(12, 6))
        sns.heatmap(
            pivot_df,
            annot=True,
            fmt=".0f",
            cmap="YlGnBu",
            cbar_kws={'label': 'Mean Salary ($)'},
            linewidths=1,
            linecolor="white"
        )

        plt.title("Advanced EDA: Heatmap of Mean Salary by Department and Position", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("IT Job Position", fontsize=12, labelpad=10)
        plt.ylabel("Department", fontsize=12, labelpad=10)
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
        plt.show()