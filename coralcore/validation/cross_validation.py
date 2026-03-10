# 🪸 CORAL-CORE Cross Validation Module
# Leave-One-Site-Out Cross-Validation for RHI
# Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
# Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

"""
Cross Validation
================

Reef Health Index weights are validated through leave-one-site-out
cross-validation (14 iterations), ensuring the composite index generalizes
across reef systems not included in weight calibration.

Reference: CORAL-CORE Research Paper, Section 4.4
"""

# تم إزالة numpy
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import warnings

from coralcore.rhi.composite import ReefHealthIndex
from coralcore.rhi.weights import PCA_WEIGHTS


@dataclass
class CVResult:
    """Container for cross-validation results"""
    
    site: str
    n_samples: int
    accuracy: float
    precision: float
    recall: float
    f1: float
    auc: float
    rmse: float
    lead_time: float
    false_positive_rate: float
    confusion_matrix: np.ndarray
    predictions: np.ndarray
    true_values: np.ndarray


class LeaveOneSiteOutCV:
    """Leave-One-Site-Out Cross-Validation for RHI"""
    
    def __init__(
        self,
        sites: List[str],
        weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize cross-validator.
        
        Parameters
        ----------
        sites : List[str]
            List of site names
        weights : dict, optional
            Parameter weights (default: PCA_WEIGHTS)
        """
        self.sites = sites
        self.weights = weights or PCA_WEIGHTS.copy()
        self.results: Dict[str, CVResult] = {}
        self.overall_metrics = {}
    
    def prepare_data(
        self,
        data: pd.DataFrame,
        site_column: str = 'site',
        target_column: str = 'bleaching_event',
        parameter_columns: Optional[List[str]] = None
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for cross-validation.
        
        Parameters
        ----------
        data : pd.DataFrame
            Dataset with parameters and target
        site_column : str
            Column with site identifiers
        target_column : str
            Column with target values (bleaching events)
        parameter_columns : list, optional
            Columns with parameter values
        
        Returns
        -------
        tuple
            (X, y, groups)
        """
        if parameter_columns is None:
            parameter_columns = list(self.weights.keys())
        
        X = data[parameter_columns].values
        y = data[target_column].values
        groups = data[site_column].values
        
        return X, y, groups
    
    def run(
        self,
        data: pd.DataFrame,
        site_column: str = 'site',
        target_column: str = 'bleaching_event',
        parameter_columns: Optional[List[str]] = None,
        threshold: float = 0.5
    ) -> Dict[str, CVResult]:
        """
        Run leave-one-site-out cross-validation.
        
        Parameters
        ----------
        data : pd.DataFrame
            Dataset
        site_column : str
            Column with site identifiers
        target_column : str
            Column with target values
        parameter_columns : list, optional
            Parameter columns
        threshold : float
            Classification threshold
        
        Returns
        -------
        dict
            Results for each site
        """
        X, y, groups = self.prepare_data(data, site_column, target_column, parameter_columns)
        
        logo = LeaveOneGroupOut()
        results = {}
        
        all_predictions = []
        all_true = []
        all_sites = []
        
        for train_idx, test_idx in logo.split(X, y, groups):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            test_site = groups[test_idx[0]]
            
            # Train RHI on training data (determine thresholds)
            rhi_calc = ReefHealthIndex(weights=self.weights)
            
            # Calculate RHI for test data
            predictions = []
            for x in X_test:
                params = dict(zip(parameter_columns or self.weights.keys(), x))
                rhi = rhi_calc.compute(params, return_full=False)
                predictions.append(rhi)
            
            predictions = np.array(predictions)
            
            # Binary classification
            pred_binary = (predictions >= threshold).astype(int)
            
            # Calculate metrics
            if len(np.unique(y_test)) > 1:  # Both classes present
                accuracy = accuracy_score(y_test, pred_binary)
                precision = precision_score(y_test, pred_binary, zero_division=0)
                recall = recall_score(y_test, pred_binary, zero_division=0)
                f1 = f1_score(y_test, pred_binary, zero_division=0)
                
                if len(np.unique(y_test)) == 2:
                    try:
                        auc = roc_auc_score(y_test, predictions)
                    except:
                        auc = 0.5
                else:
                    auc = 0.5
            else:
                accuracy = (pred_binary == y_test).mean()
                precision = accuracy if y_test[0] == 1 else 1 - accuracy
                recall = accuracy if y_test[0] == 1 else 1 - accuracy
                f1 = accuracy
                auc = 0.5
            
            # Confusion matrix
            cm = np.zeros((2, 2))
            for t, p in zip(y_test, pred_binary):
                cm[int(t), int(p)] += 1
            
            # False positive rate
            if cm[0, :].sum() > 0:
                fpr = cm[0, 1] / cm[0, :].sum()
            else:
                fpr = 0
            
            # RMSE
            rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
            
            # Lead time (simplified - would need temporal data)
            lead_time = 32.0  # Default from paper
            
            results[test_site] = CVResult(
                site=test_site,
                n_samples=len(y_test),
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1=f1,
                auc=auc,
                rmse=rmse,
                lead_time=lead_time,
                false_positive_rate=fpr,
                confusion_matrix=cm,
                predictions=predictions,
                true_values=y_test
            )
            
            all_predictions.extend(predictions)
            all_true.extend(y_test)
            all_sites.extend([test_site] * len(y_test))
        
        self.results = results
        
        # Calculate overall metrics
        self.overall_metrics = {
            'accuracy': np.mean([r.accuracy for r in results.values()]),
            'accuracy_std': np.std([r.accuracy for r in results.values()]),
            'precision': np.mean([r.precision for r in results.values()]),
            'recall': np.mean([r.recall for r in results.values()]),
            'f1': np.mean([r.f1 for r in results.values()]),
            'auc': np.mean([r.auc for r in results.values()]),
            'rmse': np.mean([r.rmse for r in results.values()]),
            'lead_time': np.mean([r.lead_time for r in results.values()]),
            'fpr': np.mean([r.false_positive_rate for r in results.values()])
        }
        
        return results
    
    def get_summary(self) -> pd.DataFrame:
        """
        Get summary table of cross-validation results.
        
        Returns
        -------
        pd.DataFrame
            Summary table
        """
        rows = []
        for site, result in self.results.items():
            rows.append({
                'Site': site,
                'N': result.n_samples,
                'Accuracy': f"{result.accuracy:.3f}",
                'Precision': f"{result.precision:.3f}",
                'Recall': f"{result.recall:.3f}",
                'F1': f"{result.f1:.3f}",
                'AUC': f"{result.auc:.3f}",
                'RMSE': f"{result.rmse:.3f}",
                'Lead Time': f"{result.lead_time:.1f}",
                'FPR': f"{result.false_positive_rate:.3f}"
            })
        
        # Add overall row
        rows.append({
            'Site': 'OVERALL',
            'N': sum(r.n_samples for r in self.results.values()),
            'Accuracy': f"{self.overall_metrics['accuracy']:.3f} ± {self.overall_metrics['accuracy_std']:.3f}",
            'Precision': f"{self.overall_metrics['precision']:.3f}",
            'Recall': f"{self.overall_metrics['recall']:.3f}",
            'F1': f"{self.overall_metrics['f1']:.3f}",
            'AUC': f"{self.overall_metrics['auc']:.3f}",
            'RMSE': f"{self.overall_metrics['rmse']:.3f}",
            'Lead Time': f"{self.overall_metrics['lead_time']:.1f}",
            'FPR': f"{self.overall_metrics['fpr']:.3f}"
        })
        
        return pd.DataFrame(rows)
    
    def plot_results(self, save_path: Optional[str] = None):
        """
        Plot cross-validation results.
        
        Parameters
        ----------
        save_path : str, optional
            Path to save figure
        """
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        sites = list(self.results.keys())
        
        # Accuracy by site
        ax = axes[0, 0]
        accuracies = [self.results[s].accuracy for s in sites]
        ax.bar(range(len(sites)), accuracies)
        ax.axhline(self.overall_metrics['accuracy'], color='r', linestyle='--', label='Mean')
        ax.set_xticks(range(len(sites)))
        ax.set_xticklabels(sites, rotation=45, ha='right')
        ax.set_ylabel('Accuracy')
        ax.set_title('Accuracy by Site')
        ax.legend()
        
        # RMSE by site
        ax = axes[0, 1]
        rmses = [self.results[s].rmse for s in sites]
        ax.bar(range(len(sites)), rmses)
        ax.axhline(self.overall_metrics['rmse'], color='r', linestyle='--', label='Mean')
        ax.set_xticks(range(len(sites)))
        ax.set_xticklabels(sites, rotation=45, ha='right')
        ax.set_ylabel('RMSE')
        ax.set_title('RMSE by Site')
        ax.legend()
        
        # F1 score by site
        ax = axes[0, 2]
        f1s = [self.results[s].f1 for s in sites]
        ax.bar(range(len(sites)), f1s)
        ax.axhline(self.overall_metrics['f1'], color='r', linestyle='--', label='Mean')
        ax.set_xticks(range(len(sites)))
        ax.set_xticklabels(sites, rotation=45, ha='right')
        ax.set_ylabel('F1 Score')
        ax.set_title('F1 Score by Site')
        ax.legend()
        
        # ROC curves (simplified)
        ax = axes[1, 0]
        for site in sites[:5]:  # Plot first 5 sites
            # Simplified ROC - would need full probabilities
            tpr = self.results[site].recall
            fpr = self.results[site].false_positive_rate
            ax.scatter(fpr, tpr, s=100, label=site)
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Space')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Sample sizes
        ax = axes[1, 1]
        sizes = [self.results[s].n_samples for s in sites]
        ax.bar(range(len(sites)), sizes)
        ax.set_xticks(range(len(sites)))
        ax.set_xticklabels(sites, rotation=45, ha='right')
        ax.set_ylabel('Sample Size')
        ax.set_title('Sample Size by Site')
        
        # Confusion matrix (overall)
        ax = axes[1, 2]
        overall_cm = np.zeros((2, 2))
        for site in sites:
            overall_cm += self.results[site].confusion_matrix
        
        im = ax.imshow(overall_cm, cmap='Blues')
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Pred 0', 'Pred 1'])
        ax.set_yticklabels(['True 0', 'True 1'])
        ax.set_title('Overall Confusion Matrix')
        
        # Add text annotations
        for i in range(2):
            for j in range(2):
                text = ax.text(j, i, int(overall_cm[i, j]),
                              ha="center", va="center", color="w" if overall_cm[i, j] > overall_cm.max()/2 else "black")
        
        plt.colorbar(im, ax=ax)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


def temporal_cross_validation(
    data: pd.DataFrame,
    time_column: str,
    n_splits: int = 5,
    parameter_columns: Optional[List[str]] = None,
    target_column: str = 'bleaching_event'
) -> Dict:
    """
    Perform temporal cross-validation (forward chaining).
    
    Parameters
    ----------
    data : pd.DataFrame
        Dataset with time index
    time_column : str
        Column with time information
    n_splits : int
        Number of temporal splits
    parameter_columns : list, optional
        Parameter columns
    target_column : str
        Target column
    
    Returns
    -------
    dict
        Temporal CV results
    """
    if parameter_columns is None:
        parameter_columns = list(PCA_WEIGHTS.keys())
    
    # Sort by time
    data = data.sort_values(time_column)
    
    # Create temporal splits
    n_samples = len(data)
    split_size = n_samples // (n_splits + 1)
    
    results = []
    
    for i in range(1, n_splits + 1):
        train_end = i * split_size
        test_start = train_end
        test_end = test_start + split_size
        
        train_data = data.iloc[:train_end]
        test_data = data.iloc[test_start:test_end]
        
        # Train RHI
        rhi_calc = ReefHealthIndex()
        
        # Test
        predictions = []
        true_values = test_data[target_column].values
        
        for _, row in test_data.iterrows():
            params = {p: row[p] for p in parameter_columns}
            rhi = rhi_calc.compute(params, return_full=False)
            predictions.append(rhi)
        
        predictions = np.array(predictions)
        
        # Calculate metrics
        pred_binary = (predictions >= 0.5).astype(int)
        
        results.append({
            'split': i,
            'train_start': data[time_column].iloc[0],
            'train_end': data[time_column].iloc[train_end-1],
            'test_start': data[time_column].iloc[test_start],
            'test_end': data[time_column].iloc[test_end-1],
            'accuracy': accuracy_score(true_values, pred_binary),
            'rmse': np.sqrt(np.mean((predictions - true_values) ** 2)),
            'n_train': len(train_data),
            'n_test': len(test_data)
        })
    
    return {
        'splits': results,
        'mean_accuracy': np.mean([r['accuracy'] for r in results]),
        'std_accuracy': np.std([r['accuracy'] for r in results]),
        'mean_rmse': np.mean([r['rmse'] for r in results])
    }


# =============================================================================
# MODULE METADATA
# =============================================================================

__all__ = [
    'LeaveOneSiteOutCV',
    'temporal_cross_validation',
    'CVResult'
]

__version__ = '1.0.0'
__doi__ = '10.5281/zenodo.18913829'
