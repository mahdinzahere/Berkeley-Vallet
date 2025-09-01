# Contributing to UC Berkeley Rideshare

Thank you for your interest in contributing to the UC Berkeley Rideshare project! This document provides guidelines and information for contributors.

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Report bugs or issues you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with code changes
- **Documentation**: Improve or add documentation
- **Testing**: Help test the application and report issues
- **Design**: Contribute to UI/UX improvements

### Before You Start

1. **Check Existing Issues**: Look through existing issues and pull requests to see if your contribution is already being worked on
2. **Read the Documentation**: Familiarize yourself with the project structure and setup
3. **Join Discussions**: Participate in GitHub Discussions to understand current priorities

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/uc-berkeley-rideshare.git
   cd uc-berkeley-rideshare
   ```

2. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install Dependencies**
   ```bash
   make dev-setup
   ```

4. **Setup AI Support**
   ```bash
   make embed-docs
   ```

5. **Start Development**
   ```bash
   make run-backend
   # In another terminal
   make run-frontend
   ```

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose

```python
def calculate_fare(distance_miles: float, base_fare: float = 2.50) -> float:
    """
    Calculate ride fare based on distance.
    
    Args:
        distance_miles: Distance in miles
        base_fare: Base fare amount
        
    Returns:
        Total fare amount
    """
    per_mile_rate = 1.75
    return base_fare + (distance_miles * per_mile_rate)
```

### JavaScript/React Native (Mobile Apps)

- Use ES6+ features
- Follow React Native best practices
- Use functional components with hooks
- Implement proper error handling

```javascript
const RideCard = ({ ride, onPress }) => {
  const handlePress = useCallback(() => {
    if (onPress) {
      onPress(ride);
    }
  }, [ride, onPress]);

  return (
    <TouchableOpacity onPress={handlePress}>
      <Text>{ride.pickup_address}</Text>
    </TouchableOpacity>
  );
};
```

### General Guidelines

- **Write Clear Commit Messages**: Use conventional commit format
- **Keep Changes Focused**: Each commit should address one specific change
- **Add Tests**: Include tests for new functionality
- **Update Documentation**: Keep README and other docs up to date

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- Write clean, well-documented code
- Add tests for new functionality
- Update relevant documentation
- Follow the existing code style

### 3. Test Your Changes

```bash
# Backend tests
make test

# Mobile app testing
cd apps/rider && npm test
cd apps/driver && npm test
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new ride matching algorithm

- Implemented improved driver-rider matching
- Added distance-based prioritization
- Updated tests for new functionality"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:

- **Clear Title**: Descriptive title for your changes
- **Description**: Detailed explanation of what you changed and why
- **Related Issues**: Link to any related issues
- **Screenshots**: If UI changes are involved
- **Testing Notes**: How you tested your changes

## Testing Guidelines

### Backend Testing

- Write unit tests for new functions
- Test API endpoints with different scenarios
- Ensure database operations work correctly
- Test error handling and edge cases

### Mobile App Testing

- Test on both iOS and Android
- Test different screen sizes
- Verify real-time functionality
- Test offline scenarios

### Testing Commands

```bash
# Backend tests
make test

# Specific test files
cd backend
python -m pytest tests/test_rides.py -v

# Mobile app testing
cd apps/rider
npm test
```

## Bug Reports

When reporting bugs, please include:

1. **Clear Description**: What happened vs. what you expected
2. **Steps to Reproduce**: Detailed steps to recreate the issue
3. **Environment**: OS, browser, app version, etc.
4. **Screenshots/Logs**: Visual evidence of the issue
5. **Additional Context**: Any relevant information

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS 13.0]
- App Version: [e.g., 1.0.0]
- Device: [e.g., iPhone 14]

## Additional Information
Any other context, logs, or screenshots
```

## Feature Requests

When requesting features:

1. **Clear Description**: What feature you want and why
2. **Use Cases**: How this feature would be used
3. **Mockups**: If applicable, include design mockups
4. **Priority**: How important this feature is to you

## Documentation Contributions

We welcome contributions to improve documentation:

- **README Updates**: Clarify setup instructions
- **API Documentation**: Improve endpoint descriptions
- **Code Comments**: Add helpful inline documentation
- **Tutorials**: Create guides for common tasks

## Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issues
- `priority: low`: Low priority issues

## Contribution Areas

### High Priority Areas

- **Testing**: Adding comprehensive test coverage
- **Documentation**: Improving setup and usage guides
- **Error Handling**: Better error messages and handling
- **Performance**: Optimizing database queries and API responses

### Good First Issues

- **Documentation**: Fix typos, clarify instructions
- **UI Improvements**: Small styling changes
- **Test Coverage**: Add tests for existing functionality
- **Bug Fixes**: Simple bug fixes

## Getting Help

If you need help contributing:

1. **Check Documentation**: Review README and other docs
2. **Search Issues**: Look for similar questions
3. **Join Discussions**: Ask in GitHub Discussions
4. **Open an Issue**: For specific problems

## Recognition

Contributors will be recognized in:

- **README**: List of contributors
- **Release Notes**: Credit for significant contributions
- **GitHub**: Contributor statistics and profile

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Checklist for Contributors

Before submitting your contribution, ensure you have:

- [ ] Read and understood the contributing guidelines
- [ ] Followed the code style guidelines
- [ ] Added appropriate tests
- [ ] Updated relevant documentation
- [ ] Tested your changes locally
- [ ] Written clear commit messages
- [ ] Created a descriptive pull request

Thank you for contributing to the UC Berkeley Rideshare project!
