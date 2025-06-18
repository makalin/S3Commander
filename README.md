# S3Commander

![S3Commander Logo](logo.png)

S3Commander is an open-source, retro terminal-style file manager for AWS S3 buckets, inspired by the classic Norton Commander. Built with a dual-pane interface, it allows users to navigate, manage, and transfer files across S3 buckets with a nostalgic, text-based UI. Designed for developers, DevOps engineers, and cloud enthusiasts, S3Commander brings a vintage feel to modern cloud storage management.

## Features

### Core Features
- **Dual-Pane Interface**: Browse two S3 buckets or prefixes side-by-side for easy file operations.
- **Retro Terminal Style**: ASCII-art inspired UI with customizable color themes (green-on-black, amber, DOS blue).
- **Keyboard-Driven**: Navigate and execute commands using classic key bindings (F3 for view, F5 for copy, etc.).
- **AWS Integration**: Supports AWS credentials via environment variables, AWS CLI profiles, or IAM roles.
- **Cross-Platform**: Runs on Windows, macOS, and Linux.

### File Operations
- **Core Operations**: List, copy, move, delete, and rename files/objects in S3 buckets.
- **Upload/Download**: Upload local files to S3 and download S3 objects to local filesystem.
- **Batch Operations**: Perform copy, move, and delete operations on multiple selected objects simultaneously.
- **Search & Filter**: Quickly find objects by name or prefix within buckets.
- **Object Management**: Create folders, rename objects, and move objects between buckets.

### Bucket Management
- **Bucket Operations**: Create and delete S3 buckets with region specification.
- **Bucket Navigation**: Browse and navigate through multiple S3 buckets.
- **Prefix Navigation**: Navigate through folder-like prefixes within buckets.

### UI & Customization
- **Theme Switching**: Change color themes at runtime (green-on-black, amber, DOS blue).
- **Status Bar**: Real-time status information and operation feedback.
- **Command Bar**: Interactive command input for file operations.
- **Selection System**: Multi-select objects for batch operations.

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

### Navigation
- **Arrow Keys**: Move cursor between objects
- **Tab**: Switch between left and right panes
- **Enter**: Enter folder/bucket or view file content
- **Space**: Toggle selection of current object
- **\\**: Change directory (navigate to specific path)

### File Operations
- **F3**: View object content (text files only)
- **F5**: Copy selected object(s) to the other pane
- **F6**: Move/rename object(s)
- **F7**: Create new folder
- **F8**: Delete selected object(s)
- **F2**: Rename current object
- **F4**: Edit object (placeholder)

### Selection & Batch Operations
- **Space**: Toggle selection of current object
- **\***: Select all objects in current pane
- **+**: Select objects by pattern (placeholder)
- **-**: Deselect all objects
- **Menu (F9)**: Access batch copy, move, and delete operations

### Menu System
Press **F9** to access the main menu with options:
1. Upload file
2. Download file
3. Create bucket
4. Delete bucket
5. Rename object
6. Move object
7. Search objects
8. Batch copy selected
9. Batch move selected
10. Batch delete selected
11. Settings (theme switching)
12. Help
0. Exit

### Settings & Customization
- **Theme Switching**: Change between green-on-black, amber, and DOS blue themes
- **Configuration**: Edit `config.json` for persistent settings
- **Logging**: Set `S3COMMANDER_LOGLEVEL` environment variable for debug output

## Configuration

Edit `config.json` to customize settings:
```json
{
  "theme": "green_on_black",
  "aws_profile": null
}
```

Available themes:
- `green_on_black`: Classic green text on black background
- `amber`: Amber/yellow text on black background
- `dos_blue`: White text on blue background (DOS style)

## Project Structure

```
S3Commander/
├── S3Commander.py          # Main application entry point
├── requirements.txt        # Python dependencies
├── config.json            # Configuration file
├── logo.png              # Project logo
├── src/
│   ├── core/
│   │   └── s3_client.py   # AWS S3 operations
│   ├── ui/
│   │   ├── interface.py   # Main UI controller
│   │   ├── themes.py      # Color theme management
│   │   ├── pane.py        # Dual-pane display
│   │   ├── status_bar.py  # Status information
│   │   └── command_bar.py # Command input
│   ├── utils/
│   │   ├── config.py      # Configuration management
│   │   └── logger.py      # Logging setup
│   └── operations/
│       └── operations.py  # Advanced operations (placeholder)
└── tests/
    ├── unit/              # Unit tests
    └── integration/       # Integration tests
```

## Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your fork and open a pull request

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Testing

Run the test suite:
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=src tests/
```

## Future Improvements

### Planned Features
- **AWS Profile/Region Switching**: Change AWS profiles and regions at runtime
- **S3-Compatible Storage**: Support for MinIO, Wasabi, DigitalOcean Spaces, and other S3-compatible services
- **Multi-Region Support**: Browse and manage buckets across different AWS regions
- **Object Metadata Viewer**: Display detailed metadata for selected objects
- **Plugin System**: Extensible architecture for custom commands and operations
- **Progress Indicators**: Progress bars for large file uploads/downloads
- **File Preview**: Preview support for images, text files, and other common formats
- **Advanced Search**: Search by file size, modification date, and other metadata
- **Accessibility**: High-contrast mode and screen reader support
- **Keyboard Shortcuts**: Customizable keyboard shortcuts
- **Operation History**: Track and replay recent operations
- **Bulk Operations**: Advanced batch operations with filters and conditions

### Technical Enhancements
- **Async Operations**: Non-blocking file operations for better performance
- **Caching**: Local cache for frequently accessed bucket listings
- **Compression**: Built-in compression for large file transfers
- **Encryption**: Client-side encryption for sensitive data
- **Multi-threading**: Parallel operations for improved performance
- **Error Recovery**: Automatic retry mechanisms for failed operations
- **Performance Monitoring**: Built-in performance metrics and monitoring

### UI/UX Improvements
- **Custom Themes**: User-defined color schemes and themes
- **Split Views**: Multiple pane configurations (3-pane, 4-pane layouts)
- **Drag & Drop**: Visual drag-and-drop interface (if terminal supports it)
- **Bookmarks**: Save frequently accessed bucket/prefix combinations
- **Favorites**: Mark frequently used buckets and objects
- **Recent Files**: Quick access to recently accessed objects
- **Context Menus**: Right-click context menus for common operations

### Integration Features
- **CloudFormation Integration**: Manage CloudFormation stack resources
- **Lambda Integration**: Direct access to Lambda function code and logs
- **CloudWatch Integration**: View and manage CloudWatch logs
- **IAM Integration**: Manage IAM policies and permissions
- **Cost Optimization**: S3 storage class recommendations and cost analysis
- **Backup Management**: Automated backup and restore operations

## Roadmap

### Version 1.1 (Next Release)
- AWS profile/region switching
- S3-compatible storage support
- Object metadata viewer
- Progress indicators for large operations

### Version 1.2
- Plugin system architecture
- Multi-region bucket management
- Advanced search capabilities
- Performance optimizations

### Version 2.0
- Complete UI redesign with modern terminal libraries
- Advanced plugin ecosystem
- Cloud service integrations
- Enterprise features

## License

S3Commander is released under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by Norton Commander and Midnight Commander
- Built with [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for AWS S3 integration
- Thanks to the open-source community for feedback and contributions

---
**Contact**: For questions or support, open an issue or join our [Discussions](https://github.com/makalin/S3Commander/discussions).
