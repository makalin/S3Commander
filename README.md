# S3Commander

S3Commander is an open-source, retro terminal-style file manager for AWS S3 buckets, inspired by the classic Norton Commander. Built with a dual-pane interface, it allows users to navigate, manage, and transfer files across S3 buckets with a nostalgic, text-based UI. Designed for developers, DevOps engineers, and cloud enthusiasts, S3Commander brings a vintage feel to modern cloud storage management.

## Features

- **Dual-Pane Interface**: Browse two S3 buckets or prefixes side-by-side for easy file operations.
- **Retro Terminal Style**: ASCII-art inspired UI with customizable color themes (e.g., green-on-black, amber, DOS blue).
- **Core Operations**: List, copy, move, delete, and rename files/objects in S3 buckets.
- **Keyboard-Driven**: Navigate and execute commands using classic key bindings (e.g., F3 for view, F5 for copy).
- **AWS Integration**: Supports AWS credentials via environment variables, AWS CLI profiles, or IAM roles.
- **Search & Filter**: Quickly find objects by name or prefix within buckets.
- **Batch Operations**: Perform actions on multiple objects simultaneously.
- **Cross-Platform**: Runs on Windows, macOS, and Linux.

## Installation

### Prerequisites
- Python 3.8+
- AWS account with S3 access
- AWS CLI configured (optional, for profile-based authentication)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/makalin/S3Commander.git
   cd S3Commander
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure AWS credentials:
   - Set environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`).
   - Or use an AWS CLI profile: `export AWS_PROFILE=your-profile-name`.

4. Run S3Commander:
   ```bash
   python S3Commander.py
   ```

## Usage

1. Launch S3Commander:
   ```bash
   python S3Commander.py
   ```

2. Navigate buckets:
   - Use arrow keys to move between objects.
   - Press `Tab` to switch between panes.
   - Enter a bucket name or prefix to navigate.

3. Common commands:
   - `F3`: View object content (text files only).
   - `F5`: Copy selected object(s) to the other pane.
   - `F6`: Move/rename object(s).
   - `F8`: Delete object(s).
   - `Ctrl+R`: Refresh bucket listing.
   - `Ctrl+F`: Search objects by name.
   - `Esc`: Exit.

4. Customize themes:
   Edit `config.json` to change the UI theme:
   ```json
   {
     "theme": "green_on_black"
   }
   ```

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your fork and open a pull request.

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Roadmap

- Add support for multi-region buckets.
- Implement file upload/download to/from local filesystem.
- Add support for S3-compatible storage (e.g., MinIO, Wasabi).
- Enhance accessibility with screen reader support.
- Introduce plugin system for custom commands.

## License

S3Commander is released under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by Norton Commander and Midnight Commander.
- Built with [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for AWS S3 integration.
- Thanks to the open-source community for feedback and contributions.

---
**Contact**: For questions or support, open an issue or join our [Discussions](https://github.com/makalin/S3Commander/discussions).
