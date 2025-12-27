# Contributing to MicroAI DAO Core

Thank you for your interest in contributing to MicroAI DAO Core. This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- - [Getting Started](#getting-started)
  - - [Development Setup](#development-setup)
    - - [Making Changes](#making-changes)
      - - [Code Standards](#code-standards)
        - - [Testing](#testing)
          - - [Pull Request Process](#pull-request-process)
            - - [Security](#security)
             
              - ## Code of Conduct
             
              - By participating in this project, you agree to maintain a respectful and inclusive environment. We are committed to providing a harassment-free experience for everyone.
             
              - ## Getting Started
             
              - ### Prerequisites
             
              - - Python 3.11+
                - - Node.js 18+ (for dashboard development)
                  - - Git
                    - - Docker (optional, for containerized development)
                     
                      - ### Fork and Clone
                     
                      - 1. Fork the repository on GitHub
                        2. 2. Clone your fork locally:
                           3.    ```bash
                                    git clone https://github.com/YOUR_USERNAME/microai-dao-core.git
                                    cd microai-dao-core
                                    ```
                                 3. Add the upstream repository:
                                 4.    ```bash
                                          git remote add upstream https://github.com/MicroAIStudios-DAO/microai-dao-core.git
                                          ```

                                       ## Development Setup

                                   ### Python Environment

                             ```bash
                             # Create virtual environment
                             python -m venv venv
                             source venv/bin/activate  # On Windows: venv\Scripts\activate

                             # Install dependencies
                             pip install -r requirements.txt
                             pip install -r requirements-dev.txt  # Development dependencies

                             # Initialize database
                             python database/init_db.py

                             # Verify installation
                             pytest tests/unit/ -v
                             ```

                             ### Dashboard Development

                           ```bash
                           cd microai-dashboard
                           npm install
                           npm run dev
                           ```

                           ### Environment Variables

                           Copy the example environment file and configure:

                           ```bash
                           cp .env.example .env
                           # Edit .env with your configuration
                           ```

                           Required variables:
                           - `JWT_SECRET_KEY` - Secret key for JWT tokens
                           - - `TRUST_SIGNING_KEY` - Key for trust stack signing
                             - - `DATABASE_URL` - Database connection string
                              
                               - ## Making Changes
                              
                               - ### Branch Naming
                              
                               - Use descriptive branch names following this convention:
                              
                               - - `feature/` - New features (e.g., `feature/guardian-dashboard`)
                                 - - `fix/` - Bug fixes (e.g., `fix/epi-calculation-error`)
                                   - - `docs/` - Documentation updates (e.g., `docs/api-reference`)
                                     - - `refactor/` - Code refactoring (e.g., `refactor/trust-metrics`)
                                       - - `test/` - Test additions/updates (e.g., `test/policy-validator`)
                                        
                                         - ### Creating a Branch
                                        
                                         - ```bash
                                           git checkout main
                                           git pull upstream main
                                           git checkout -b feature/your-feature-name
                                           ```

                                           ## Code Standards

                                           ### Python

                                           - Follow [PEP 8](https://pep8.org/) style guide
                                           - - Use [Black](https://black.readthedocs.io/) for code formatting
                                             - - Use type hints for function signatures
                                               - - Maximum line length: 88 characters
                                                
                                                 - ```bash
                                                   # Format code
                                                   black src/

                                                   # Check formatting
                                                   black --check src/

                                                   # Lint code
                                                   flake8 src/
                                                   ```

                                                   ### TypeScript (Dashboard)

                                                   - Follow the project's ESLint configuration
                                                   - - Use TypeScript strict mode
                                                     - - Prefer functional components with hooks
                                                      
                                                       - ```bash
                                                         cd microai-dashboard
                                                         npm run lint
                                                         npm run lint:fix
                                                         ```

                                                         ### Commit Messages

                                                         Use [Conventional Commits](https://www.conventionalcommits.org/) format:

                                                         ```
                                                         type(scope): description

                                                         [optional body]

                                                         [optional footer]
                                                         ```

                                                         Types:
                                                         - `feat` - New feature
                                                         - - `fix` - Bug fix
                                                           - - `docs` - Documentation only
                                                             - - `style` - Formatting, no code change
                                                               - - `refactor` - Code restructuring
                                                                 - - `test` - Adding/updating tests
                                                                   - - `chore` - Maintenance tasks
                                                                    
                                                                     - Examples:
                                                                     - ```
                                                                       feat(epi): add harmonic mean calculation for ethics scores
                                                                       fix(voter): resolve vote history tracking issue
                                                                       docs(api): update endpoint documentation
                                                                       ```

                                                                       ## Testing

                                                                       ### Running Tests

                                                                       ```bash
                                                                       # All unit tests
                                                                       pytest tests/unit/ -v

                                                                       # Specific test file
                                                                       pytest tests/unit/test_epi_calculator.py -v

                                                                       # With coverage
                                                                       pytest tests/unit/ --cov=src --cov-report=html

                                                                       # Integration tests (requires API running)
                                                                       pytest tests/integration/ -v
                                                                       ```

                                                                       ### Writing Tests

                                                                       - Place tests in the appropriate directory under `tests/`
                                                                       - - Name test files with `test_` prefix
                                                                         - - Use descriptive test function names
                                                                           - - Include docstrings explaining test purpose
                                                                            
                                                                             - Example:
                                                                             - ```python
                                                                               def test_epi_calculator_returns_valid_score():
                                                                                   """Test that EPI calculator returns a score between 0 and 1."""
                                                                                   calculator = EPICalculator()
                                                                                   scores = EPIScores(profit=0.8, ethics=0.7, violations=[])
                                                                                   result = calculator.compute_epi(scores)
                                                                                   assert 0 <= result.epi_score <= 1
                                                                               ```

                                                                               ## Pull Request Process

                                                                               ### Before Submitting

                                                                               1. Ensure all tests pass locally
                                                                               2. 2. Update documentation if needed
                                                                                  3. 3. Add tests for new functionality
                                                                                     4. 4. Run linting and formatting checks
                                                                                        5. 5. Rebase on latest main if needed
                                                                                          
                                                                                           6. ### Submitting a PR
                                                                                          
                                                                                           7. 1. Push your branch to your fork:
                                                                                              2.    ```bash
                                                                                                       git push origin feature/your-feature-name
                                                                                                       ```
                                                                                                    
                                                                                                    2. Create a Pull Request on GitHub
                                                                                                
                                                                                                    3. 3. Fill out the PR template with:
                                                                                                       4.    - Description of changes
                                                                                                             -    - Related issue numbers
                                                                                                                  -    - Testing performed
                                                                                                                       -    - Screenshots (if UI changes)
                                                                                                                        
                                                                                                                            - ### Review Process
                                                                                                                        
                                                                                                                            - - PRs require at least one approval before merging
                                                                                                                              - - Address review feedback promptly
                                                                                                                                - - Keep PRs focused and reasonably sized
                                                                                                                                  - - Squash commits before merging if requested
                                                                                                                                   
                                                                                                                                    - ## Security
                                                                                                                                   
                                                                                                                                    - ### Reporting Vulnerabilities
                                                                                                                                   
                                                                                                                                    - **Do NOT create public GitHub issues for security vulnerabilities.**
                                                                                                                                   
                                                                                                                                    - Please report security issues to: security@microaistudios.io
                                                                                                                                   
                                                                                                                                    - See [SECURITY.md](SECURITY.md) for our full security policy.
                                                                                                                                   
                                                                                                                                    - ### Security Best Practices
                                                                                                                                   
                                                                                                                                    - - Never commit secrets or API keys
                                                                                                                                      - - Use environment variables for sensitive configuration
                                                                                                                                        - - Follow the principle of least privilege
                                                                                                                                          - - Keep dependencies updated
                                                                                                                                           
                                                                                                                                            - ## Questions?
                                                                                                                                           
                                                                                                                                            - - Open a [Discussion](https://github.com/MicroAIStudios-DAO/microai-dao-core/discussions) for general questions
                                                                                                                                              - - Create an [Issue](https://github.com/MicroAIStudios-DAO/microai-dao-core/issues) for bug reports or feature requests
                                                                                                                                                - - Review existing issues and PRs before creating new ones
                                                                                                                                                 
                                                                                                                                                  - ---
                                                                                                                                                  
                                                                                                                                                  Thank you for contributing to MicroAI DAO Core!
