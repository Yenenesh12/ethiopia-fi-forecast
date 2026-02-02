"""
Visualization utilities for Ethiopia Financial Inclusion EDA
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class VisualizationUtils:
    """Utility class for creating standardized visualizations"""
    
    def __init__(self):
        self.setup_style()
    
    def setup_style(self):
        """Set up consistent plotting style"""
        plt.style.use('default')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 9
    
    def create_trend_plot(self, df: pd.DataFrame, x_col: str, y_col: str, 
                         group_col: Optional[str] = None, title: str = "Trend Analysis",
                         figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """Create a trend line plot with optional grouping"""
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if group_col and group_col in df.columns:
            for group in df[group_col].unique():
                if pd.notna(group):
                    data = df[df[group_col] == group]
                    ax.plot(data[x_col], data[y_col], marker='o', 
                           label=str(group), linewidth=2, markersize=6)
            ax.legend()
        else:
            ax.plot(df[x_col], df[y_col], marker='o', 
                   linewidth=3, markersize=8, color='#2E86AB')
        
        ax.set_title(title, fontweight='bold', pad=20)
        ax.set_xlabel(x_col.replace('_', ' ').title())
        ax.set_ylabel(y_col.replace('_', ' ').title())
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_comparison_bar(self, data: Dict, title: str = "Comparison",
                             figsize: Tuple[int, int] = (10, 6),
                             horizontal: bool = False) -> plt.Figure:
        """Create a bar chart for comparisons"""
        
        fig, ax = plt.subplots(figsize=figsize)
        
        keys = list(data.keys())
        values = list(data.values())
        
        colors = sns.color_palette("husl", len(keys))
        
        if horizontal:
            bars = ax.barh(keys, values, color=colors, alpha=0.8)
            ax.set_xlabel('Value')
        else:
            bars = ax.bar(keys, values, color=colors, alpha=0.8)
            ax.set_ylabel('Value')
            plt.xticks(rotation=45, ha='right')
        
        ax.set_title(title, fontweight='bold', pad=20)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            if horizontal:
                ax.text(value + max(values) * 0.01, bar.get_y() + bar.get_height()/2, 
                       f'{value:.1f}', va='center', ha='left')
            else:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.01,
                       f'{value:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def create_distribution_plot(self, df: pd.DataFrame, col: str, 
                               group_col: Optional[str] = None,
                               title: str = "Distribution Analysis",
                               figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """Create distribution plots (histogram/boxplot)"""
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle(title, fontsize=14, fontweight='bold')
        
        # Histogram
        if group_col and group_col in df.columns:
            groups = df[group_col].unique()
            colors = sns.color_palette("husl", len(groups))
            
            for i, group in enumerate(groups):
                if pd.notna(group):
                    data = df[df[group_col] == group][col].dropna()
                    axes[0].hist(data, alpha=0.7, label=str(group), 
                               color=colors[i], bins=15)
            axes[0].legend()
        else:
            axes[0].hist(df[col].dropna(), bins=15, alpha=0.7, color='#2E86AB')
        
        axes[0].set_title('Distribution')
        axes[0].set_xlabel(col.replace('_', ' ').title())
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        # Boxplot
        if group_col and group_col in df.columns:
            df_clean = df[[col, group_col]].dropna()
            sns.boxplot(data=df_clean, x=group_col, y=col, ax=axes[1])
            axes[1].tick_params(axis='x', rotation=45)
        else:
            axes[1].boxplot(df[col].dropna())
            axes[1].set_xticklabels(['All Data'])
        
        axes[1].set_title('Box Plot')
        axes[1].set_ylabel(col.replace('_', ' ').title())
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_correlation_heatmap(self, df: pd.DataFrame, 
                                  title: str = "Correlation Matrix",
                                  figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """Create correlation heatmap for numeric columns"""
        
        # Select only numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("⚠️ Not enough numeric columns for correlation analysis")
            return None
        
        corr_matrix = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, ax=ax, cbar_kws={'shrink': 0.8})
        
        ax.set_title(title, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig
    
    def create_multi_metric_dashboard(self, metrics: Dict, 
                                    title: str = "Key Metrics Dashboard",
                                    figsize: Tuple[int, int] = (16, 10)) -> plt.Figure:
        """Create a dashboard with multiple metrics"""
        
        n_metrics = len(metrics)
        cols = min(3, n_metrics)
        rows = (n_metrics + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        if n_metrics == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes if isinstance(axes, (list, np.ndarray)) else [axes]
        else:
            axes = axes.flatten()
        
        colors = sns.color_palette("husl", n_metrics)
        
        for i, (metric_name, metric_data) in enumerate(metrics.items()):
            ax = axes[i]
            
            if isinstance(metric_data, dict):
                # Bar chart for dictionary data
                keys = list(metric_data.keys())
                values = list(metric_data.values())
                ax.bar(keys, values, color=colors[i], alpha=0.8)
                ax.set_title(metric_name, fontweight='bold')
                ax.tick_params(axis='x', rotation=45)
            
            elif isinstance(metric_data, (list, pd.Series, np.ndarray)):
                # Histogram for array-like data
                ax.hist(metric_data, bins=15, color=colors[i], alpha=0.8)
                ax.set_title(metric_name, fontweight='bold')
            
            else:
                # Single value display
                ax.text(0.5, 0.5, f'{metric_data:.2f}', 
                       ha='center', va='center', fontsize=24, fontweight='bold',
                       transform=ax.transAxes)
                ax.set_title(metric_name, fontweight='bold')
                ax.set_xticks([])
                ax.set_yticks([])
            
            ax.grid(True, alpha=0.3)
        
        # Hide unused subplots
        for i in range(n_metrics, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig: plt.Figure, filename: str, 
                   output_dir: str = "../reports/figures/") -> None:
        """Save figure to file"""
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"📊 Figure saved: {filepath}")