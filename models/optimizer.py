def optimize(self):
        """Run the portfolio optimization."""
        self._validate_inputs()
        
        n_assets = len(self.symbols)
        initial_weights = np.ones(n_assets) / n_assets  # Equal weights to start
        
        objective_function = self._get_objective_function()
        constraints = self._get_constraints()
        bounds = self._get_bounds()
        
        # Set up optimization start time for tracking
        start_time = time.time()
        
        # Run the optimization
        result = minimize(
            objective_function,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000, 'ftol': 1e-6, 'disp': False}
        )
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        if not result.success:
            raise RuntimeError(f"Optimization failed: {result.message}")
        
        # Store the result
        weights = result.x
        
        # Ensure weights sum to 1 (may have small floating point errors)
        weights = weights / np.sum(weights)
        
        # Calculate portfolio return and risk
        portfolio_return = np.sum(self.returns * weights)
        portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        
        # Calculate Sharpe ratio
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_risk
        
        # Store the results
        self.last_result = {
            'weights': {self.symbols[i]: weights[i] for i in range(n_assets)},
            'return': portfolio_return,
            'risk': portfolio_risk,
            'sharpe_ratio': sharpe_ratio,
            'execution_time': execution_time,
            'success': result.success,
            'message': result.message,
            'iterations': result.nit
        }
        
        return self.last_result
    
    def get_efficient_frontier(self, points=50):
        """Generate efficient frontier data points."""
        self._validate_inputs()
        
        n_assets = len(self.symbols)
        
        # Define the range of target returns
        min_return = min(self.returns)
        max_return = max(self.returns)
        target_returns = np.linspace(min_return, max_return, points)
        
        # Store the results
        frontier = []
        
        # Save original constraints and target
        original_constraints = self.constraints.copy()
        original_target = self.optimization_target
        
        # Set optimization target to minimize risk
        self.set_optimization_target("min_risk")
        
        for target_return in target_returns:
            # Add target return constraint
            self.constraints['target_return'] = target_return
            
            try:
                result = self.optimize()
                frontier.append({
                    'return': result['return'],
                    'risk': result['risk'],
                    'sharpe_ratio': result['sharpe_ratio']
                })
            except Exception as e:
                # Skip points that can't be optimized
                pass
        
        # Restore original constraints and target
        self.constraints = original_constraints
        self.set_optimization_target(original_target)
        
        return frontier
    
    def get_optimal_portfolio(self):
        """Get the optimal portfolio based on the optimization target."""
        if self.last_result is None:
            self.optimize()
        
        return self.last_result# models/optimizer.py - Portfolio optimization engine

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import time

class PortfolioOptimizer:
    """Portfolio optimization engine."""
    
    def __init__(self):
        """Initialize the optimizer."""
        self.returns = None
        self.cov_matrix = None
        self.symbols = []
        self.constraints = {}
        self.optimization_target = "max_return"  # Default target
        self.risk_free_rate = 0.035  # 3.5% annual
        self.last_result = None
        
    def set_returns(self, returns_data):
        """Set the expected returns for the assets."""
        self.returns = returns_data
        
    def set_covariance_matrix(self, cov_matrix):
        """Set the covariance matrix for the assets."""
        self.cov_matrix = cov_matrix
        
    def set_symbols(self, symbols):
        """Set the asset symbols."""
        self.symbols = symbols
        
    def set_optimization_target(self, target):
        """Set the optimization target."""
        valid_targets = ["max_return", "min_risk", "max_sharpe"]
        if target not in valid_targets:
            raise ValueError(f"Invalid target: {target}. Must be one of {valid_targets}")
        self.optimization_target = target
        
    def set_constraints(self, constraints):
        """Set optimization constraints."""
        self.constraints = constraints
        
    def set_risk_free_rate(self, rate):
        """Set the risk-free rate."""
        self.risk_free_rate = rate
        
    def _validate_inputs(self):
        """Validate that all necessary inputs are provided."""
        if self.returns is None:
            raise ValueError("Expected returns not set")
        
        if self.cov_matrix is None:
            raise ValueError("Covariance matrix not set")
        
        if len(self.symbols) == 0:
            raise ValueError("Asset symbols not set")
        
        if len(self.returns) != len(self.symbols):
            raise ValueError("Number of returns must match number of symbols")
        
        if self.cov_matrix.shape[0] != len(self.symbols) or self.cov_matrix.shape[1] != len(self.symbols):
            raise ValueError("Covariance matrix dimensions must match number of symbols")
    
    def _maximize_return(self, weights):
        """Objective function to maximize return."""
        return -np.sum(self.returns * weights)
    
    def _minimize_risk(self, weights):
        """Objective function to minimize risk (volatility)."""
        return np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
    
    def _maximize_sharpe(self, weights):
        """Objective function to maximize Sharpe ratio."""
        portfolio_return = np.sum(self.returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        
        # Check for zero volatility to avoid division by zero
        if portfolio_volatility == 0:
            return 0
        
        return -(portfolio_return - self.risk_free_rate) / portfolio_volatility
    
    def _get_objective_function(self):
        """Get the appropriate objective function based on the target."""
        if self.optimization_target == "max_return":
            return self._maximize_return
        elif self.optimization_target == "min_risk":
            return self._minimize_risk
        elif self.optimization_target == "max_sharpe":
            return self._maximize_sharpe
        else:
            raise ValueError(f"Unknown optimization target: {self.optimization_target}")
    
    def _get_constraints(self):
        """Build the constraints for the optimization problem."""
        # Weight sum constraint (weights must sum to 1)
        constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - a1}]
        
        # Handle min/max position constraints
        if 'min_position' in self.constraints:
            min_position = self.constraints['min_position']
            constraints.append({
                'type': 'ineq', 
                'fun': lambda weights: weights - min_position
            })
            
        if 'max_position' in self.constraints:
            max_position = self.constraints['max_position']
            constraints.append({
                'type': 'ineq', 
                'fun': lambda weights: max_position - weights
            })
            
        # Handle volatility constraint
        if 'max_volatility' in self.constraints:
            max_vol = self.constraints['max_volatility']
            constraints.append({
                'type': 'ineq',
                'fun': lambda weights: max_vol - np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            })
            
        # Handle target return constraint
        if 'target_return' in self.constraints:
            target_return = self.constraints['target_return']
            constraints.append({
                'type': 'eq',
                'fun': lambda weights: np.sum(self.returns * weights) - target_return
            })
            
        return constraints
    
    def _get_bounds(self):
        """Get the bounds for each weight."""
        n_assets = len(self.symbols)
        
        # Default bounds (0 to 1)
        bounds = [(0, 1) for _ in range(n_assets)]
        
        # Handle custom bounds for each asset
        if 'asset_bounds' in self.constraints:
            asset_bounds = self.constraints['asset_bounds']
            for i, symbol in enumerate(self.symbols):
                if symbol in asset_bounds:
                    bounds[i] = asset_bounds[symbol]
                    
        return bounds