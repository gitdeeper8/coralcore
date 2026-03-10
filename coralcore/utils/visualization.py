# 🪸 CORAL-CORE Visualization Utilities
# Plotting functions for RHI and parameter visualization
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""
Visualization Utilities
=======================

Utilities for visualizing RHI time series, parameter contributions,
acoustic signatures, and photogrammetry data.
"""

# تم إزالة numpy
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
import warnings

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
import seaborn as sns

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    from mpl_toolkits.mplot3d import Axes3D
    MPL3D_AVAILABLE = True
except ImportError:
    MPL3D_AVAILABLE = False


# =============================================================================
# CONSTANTS
# =============================================================================

# Color schemes
RHI_COLORS = {
    'healthy': '#2ecc71',  # Green
    'stressed': '#f39c12',  # Orange
    'critical': '#e74c3c',  # Red
    'background': '#ecf0f1',  # Light gray
    'grid': '#bdc3c7'  # Gray
}

PARAMETER_COLORS = {
    'g_ca': '#3498db',  # Blue
    'e_diss': '#9b59b6',  # Purple
    'phi_ps': '#2ecc71',  # Green
    'rho_skel': '#e67e22',  # Orange
    'delta_ph': '#f1c40f',  # Yellow
    's_reef': '#1abc9c',  # Turquoise
    'k_s': '#e74c3c',  # Red
    't_thr': '#34495e'  # Dark blue
}

# Plot styles
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


# =============================================================================
# RHI VISUALIZATION
# =============================================================================

def plot_rhi_timeseries(
    timestamps: List[datetime],
    rhi_values: np.ndarray,
    station_name: str = "",
    save_path: Optional[str] = None,
    show_thresholds: bool = True,
    figsize: Tuple[int, int] = (12, 6)
):
    """
    Plot RHI time series with health thresholds.
    
    Parameters
    ----------
    timestamps : List[datetime]
        Time points
    rhi_values : np.ndarray
        RHI values
    station_name : str
        Station name for title
    save_path : str, optional
        Path to save figure
    show_thresholds : bool
        Show health thresholds
    figsize : tuple
        Figure size
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot RHI
    ax.plot(timestamps, rhi_values, 'b-', linewidth=2, label='RHI')
    ax.fill_between(timestamps, 0, rhi_values, alpha=0.3, color='blue')
    
    if show_thresholds:
        # Add threshold lines
        ax.axhline(y=0.8, color=RHI_COLORS['healthy'], linestyle='--', alpha=0.7, label='Healthy (≥0.8)')
        ax.axhline(y=0.5, color=RHI_COLORS['stressed'], linestyle='--', alpha=0.7, label='Stressed (0.5-0.79)')
        
        # Color regions
        ax.axhspan(0.8, 1.0, alpha=0.2, color=RHI_COLORS['healthy'])
        ax.axhspan(0.5, 0.8, alpha=0.2, color=RHI_COLORS['stressed'])
        ax.axhspan(0.0, 0.5, alpha=0.2, color=RHI_COLORS['critical'])
    
    # Formatting
    ax.set_xlabel('Date')
    ax.set_ylabel('Reef Health Index (RHI)')
    ax.set_title(f'RHI Time Series - {station_name}')
    ax.set_ylim(0, 1)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Format dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_rhi_contributions(
    rhi_result,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
):
    """
    Plot parameter contributions to RHI.
    
    Parameters
    ----------
    rhi_result : RHIResult
        RHI calculation result
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Normalized parameters
    params = list(rhi_result.normalized_params.keys())
    norm_values = list(rhi_result.normalized_params.values())
    colors = [PARAMETER_COLORS.get(p, '#95a5a6') for p in params]
    
    ax1.barh(params, norm_values, color=colors)
    ax1.set_xlabel('Normalized Value')
    ax1.set_title('Parameter Values (Normalized)')
    ax1.set_xlim(0, 1)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Contributions
    contributions = list(rhi_result.contributions.values())
    
    wedges, texts, autotexts = ax2.pie(
        contributions,
        labels=params,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    ax2.set_title(f'Parameter Contributions\nRHI = {rhi_result.rhi:.3f}')
    
    plt.suptitle(f'RHI Analysis - {rhi_result.status}', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_rhi_heatmap(
    data: pd.DataFrame,
    station_col: str = 'station',
    time_col: str = 'timestamp',
    rhi_col: str = 'rhi',
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None
):
    """
    Create heatmap of RHI across stations and time.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data with RHI values
    station_col : str
        Column with station names
    time_col : str
        Column with timestamps
    rhi_col : str
        Column with RHI values
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    # Pivot table
    pivot = data.pivot_table(
        index=station_col,
        columns=pd.to_datetime(data[time_col]).dt.date,
        values=rhi_col
    )
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create heatmap
    im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    # Formatting
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Station')
    ax.set_title('RHI Heatmap Across Stations')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('RHI')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


# =============================================================================
# PARAMETER VISUALIZATION
# =============================================================================

def plot_parameter_timeseries(
    data: pd.DataFrame,
    parameters: List[str],
    timestamps: Optional[List[datetime]] = None,
    station_name: str = "",
    figsize: Tuple[int, int] = (15, 10),
    save_path: Optional[str] = None
):
    """
    Plot time series for multiple parameters.
    
    Parameters
    ----------
    data : pd.DataFrame
        Parameter data
    parameters : List[str]
        Parameters to plot
    timestamps : List[datetime], optional
        Time points
    station_name : str
        Station name
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    n_params = len(parameters)
    fig, axes = plt.subplots(n_params, 1, figsize=figsize, sharex=True)
    
    if n_params == 1:
        axes = [axes]
    
    for i, param in enumerate(parameters):
        ax = axes[i]
        
        if param in data.columns:
            values = data[param].values
            
            if timestamps is not None:
                ax.plot(timestamps, values, color=PARAMETER_COLORS.get(param, 'blue'), linewidth=1.5)
            else:
                ax.plot(values, color=PARAMETER_COLORS.get(param, 'blue'), linewidth=1.5)
            
            # Fill missing
            if timestamps is not None:
                mask = pd.isna(values)
                if mask.any():
                    ax.fill_between(
                        np.array(timestamps)[mask],
                        0, 1,
                        color='gray',
                        alpha=0.3,
                        label='Missing'
                    )
        
        ax.set_ylabel(param)
        ax.grid(True, alpha=0.3)
        ax.legend([param])
    
    if timestamps is not None:
        axes[-1].set_xlabel('Date')
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=45)
    
    plt.suptitle(f'Parameter Time Series - {station_name}', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_correlation_matrix(
    data: pd.DataFrame,
    parameters: List[str],
    figsize: Tuple[int, int] = (10, 8),
    save_path: Optional[str] = None
):
    """
    Plot correlation matrix of parameters.
    
    Parameters
    ----------
    data : pd.DataFrame
        Parameter data
    parameters : List[str]
        Parameters to include
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    # Compute correlation matrix
    corr = data[parameters].corr()
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.2f',
        cmap='RdBu_r',
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        ax=ax,
        cbar_kws={'label': 'Correlation'}
    )
    
    ax.set_title('Parameter Correlation Matrix')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


# =============================================================================
# ACOUSTIC VISUALIZATION
# =============================================================================

def plot_spectrogram(
    audio: np.ndarray,
    sr: int = 96000,
    ax: Optional[plt.Axes] = None,
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None
):
    """
    Plot audio spectrogram.
    
    Parameters
    ----------
    audio : np.ndarray
        Audio time series
    sr : int
        Sampling rate
    ax : plt.Axes, optional
        Axes to plot on
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    
    # Compute spectrogram
    from coralcore.utils.acoustics import compute_spectrogram
    S_db, freqs, times = compute_spectrogram(audio, sr)
    
    # Plot
    im = ax.pcolormesh(
        times,
        freqs / 1000,  # Convert to kHz
        S_db,
        shading='gouraud',
        cmap='viridis'
    )
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (kHz)')
    ax.set_title('Acoustic Spectrogram')
    ax.set_ylim(0, 24)  # Up to 24 kHz
    
    # Colorbar
    plt.colorbar(im, ax=ax, label='Power (dB)')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_acoustic_features(
    features,
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None
):
    """
    Plot extracted acoustic features.
    
    Parameters
    ----------
    features : AcousticFeatures
        Extracted acoustic features
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(3, 3, figure=fig)
    
    # Spectrogram
    ax1 = fig.add_subplot(gs[0, :])
    im = ax1.pcolormesh(
        features.times,
        features.frequencies / 1000,
        features.spectrogram,
        shading='gouraud',
        cmap='viridis'
    )
    ax1.set_ylabel('Frequency (kHz)')
    ax1.set_title('Spectrogram')
    ax1.set_ylim(0, 24)
    plt.colorbar(im, ax=ax1, label='dB')
    
    # Band powers
    ax2 = fig.add_subplot(gs[1, 0])
    bands = list(features.band_powers.keys())
    powers = list(features.band_powers.values())
    ax2.barh(bands, powers, color='skyblue')
    ax2.set_xlabel('Power (dB)')
    ax2.set_title('Band Powers')
    
    # MFCCs
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.bar(range(len(features.mfccs)), features.mfccs, color='lightgreen')
    ax3.set_xlabel('MFCC Coefficient')
    ax3.set_ylabel('Value')
    ax3.set_title('MFCCs')
    
    # Indices
    ax4 = fig.add_subplot(gs[1, 2])
    indices = {
        'Shannon': features.shannon_entropy,
        'ACI': features.aci,
        'BI': features.bi,
        'NDSI': features.ndsi
    }
    ax4.bar(indices.keys(), indices.values(), color='lightcoral')
    ax4.set_ylabel('Value')
    ax4.set_title('Acoustic Indices')
    
    # Spectral centroid over time (simplified)
    ax5 = fig.add_subplot(gs[2, :])
    ax5.plot([features.spectral_centroid] * 10, 'r-', linewidth=2)
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Frequency (Hz)')
    ax5.set_title(f'Spectral Centroid: {features.spectral_centroid:.1f} Hz')
    ax5.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


# =============================================================================
# 3D VISUALIZATION
# =============================================================================

def plot_3d_mesh(
    vertices: np.ndarray,
    faces: Optional[np.ndarray] = None,
    colors: Optional[np.ndarray] = None,
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None
):
    """
    Plot 3D mesh from photogrammetry.
    
    Parameters
    ----------
    vertices : np.ndarray
        Mesh vertices (N, 3)
    faces : np.ndarray, optional
        Mesh faces (M, 3)
    colors : np.ndarray, optional
        Vertex colors
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    if not MPL3D_AVAILABLE:
        raise ImportError("mpl_toolkits.mplot3d is required for 3D plotting")
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    
    if faces is not None and len(faces) > 0:
        # Plot mesh as triangles
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        
        # Create triangles
        triangles = vertices[faces]
        
        if colors is not None:
            # Use vertex colors
            face_colors = np.mean(colors[faces], axis=1)
            mesh = Poly3DCollection(triangles, facecolors=face_colors, alpha=0.8)
        else:
            mesh = Poly3DCollection(triangles, alpha=0.8, linewidths=0.1, edgecolors='black')
        
        ax.add_collection3d(mesh)
    else:
        # Plot as point cloud
        if colors is not None:
            ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c=colors, s=1, alpha=0.5)
        else:
            ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=1, alpha=0.5)
    
    # Set labels
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('3D Reef Reconstruction')
    
    # Equal aspect
    max_range = np.ptp(vertices, axis=0).max() / 2
    mid = np.mean(vertices, axis=0)
    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


# =============================================================================
# PLOTLY DASHBOARD (Interactive)
# =============================================================================

def create_interactive_dashboard(
    data: pd.DataFrame,
    station_name: str = "",
    output_file: Optional[str] = None
):
    """
    Create interactive Plotly dashboard.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data with parameters and RHI
    station_name : str
        Station name
    output_file : str, optional
        HTML output file
    
    Returns
    -------
    plotly.graph_objects.Figure
        Interactive dashboard
    """
    if not PLOTLY_AVAILABLE:
        raise ImportError("plotly is required for interactive dashboard")
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('RHI Time Series', 'Parameter Contributions',
                       'Parameter Trends', 'Correlation Heatmap',
                       'Acoustic Signature', 'Recent Alerts'),
        specs=[[{'secondary_y': False}, {'type': 'pie'}],
               [{'secondary_y': True}, {'type': 'heatmap'}],
               [{'type': 'scatter'}, {'type': 'table'}]]
    )
    
    # RHI Time Series
    if 'timestamp' in data.columns and 'rhi' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data['timestamp'],
                y=data['rhi'],
                mode='lines+markers',
                name='RHI',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # Add threshold lines
        fig.add_hline(y=0.8, line_dash="dash", line_color="green", 
                     annotation_text="Healthy", row=1, col=1)
        fig.add_hline(y=0.5, line_dash="dash", line_color="orange",
                     annotation_text="Stressed", row=1, col=1)
    
    # Parameter contributions (pie chart)
    if 'rhi' in data.columns and len(data) > 0:
        # Get latest RHI result
        from coralcore.rhi.composite import ReefHealthIndex
        rhi_calc = ReefHealthIndex()
        
        params = {p: data[p].iloc[-1] for p in rhi_calc.weights.keys() if p in data.columns}
        if len(params) == 8:
            result = rhi_calc.compute(params, return_full=True)
            
            fig.add_trace(
                go.Pie(
                    labels=list(result.contributions.keys()),
                    values=list(result.contributions.values()),
                    name='Contributions'
                ),
                row=1, col=2
            )
    
    # Parameter trends
    for i, param in enumerate(['g_ca', 'phi_ps', 'e_diss']):
        if param in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data['timestamp'],
                    y=data[param],
                    mode='lines',
                    name=param,
                    line=dict(color=list(PARAMETER_COLORS.values())[i])
                ),
                row=2, col=1
            )
    
    # Correlation heatmap
    param_cols = [c for c in data.columns if c in PARAMETER_COLORS]
    if len(param_cols) > 1:
        corr = data[param_cols].corr()
        
        fig.add_trace(
            go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                colorscale='RdBu',
                zmid=0,
                text=corr.values,
                texttemplate='%{text:.2f}',
                textfont={"size": 10},
                name='Correlation'
            ),
            row=2, col=2
        )
    
    # Update layout
    fig.update_layout(
        title=f'CORAL-CORE Interactive Dashboard - {station_name}',
        height=900,
        showlegend=True,
        template='plotly_white'
    )
    
    # Update axes
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text="RHI", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=1)
    
    if output_file:
        fig.write_html(output_file)
    
    return fig


# =============================================================================
# MODULE METADATA
# =============================================================================

__all__ = [
    'plot_rhi_timeseries',
    'plot_rhi_contributions',
    'plot_rhi_heatmap',
    'plot_parameter_timeseries',
    'plot_correlation_matrix',
    'plot_spectrogram',
    'plot_acoustic_features',
    'plot_3d_mesh',
    'create_interactive_dashboard',
    'RHI_COLORS',
    'PARAMETER_COLORS'
]

__version__ = '1.0.0'
__doi__ = '10.5281/zenodo.18913829'
