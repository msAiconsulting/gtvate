# 🎵 Acoustic Sensor POC Dashboard

A comprehensive proof-of-concept dashboard showcasing revolutionary acoustic sensor technology with real-time data visualization and analysis capabilities.

## 🚀 Features

### Core Capabilities
- **Wide Frequency Range Analysis**: 25Hz to 10kHz spectrum monitoring
- **High Precision Sensing**: Sub-second temporal resolution
- **Multi-Parameter Monitoring**: Pressure, acoustic, and level measurements
- **Real-time Visualization**: Interactive plots and dynamic updates
- **Comprehensive Analytics**: Statistical summaries and trend analysis

### Dashboard Components
1. **📊 Overview Tab**: System-wide sensor status and pressure monitoring
2. **🎵 Acoustic Analysis**: Frequency spectrum analysis and heatmap visualization
3. **📏 Level Monitoring**: Level contact and ambient condition tracking
4. **🔧 Technical Details**: Comprehensive specifications and statistics

## 📊 Data Sources

### Acoustic Sensor (AC01-1400057)
- **Frequency Bands**: 31 discrete frequency measurements
- **Sampling Rate**: 1Hz continuous monitoring
- **Data Points**: 14,377+ records with timestamp precision
- **Additional Parameters**: Level contact and ambient readings

### Pressure Sensors
- **Total Pressure**: Upstream and downstream measurements
- **Static Pressure**: Upstream and downstream static readings
- **Range**: 0-50,000 psi with ±0.1% accuracy
- **Response Time**: <10ms for real-time monitoring

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
- `gradio>=4.0.0` - Web interface framework
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `plotly>=5.15.0` - Interactive plotting
- `matplotlib>=3.7.0` - Plotting library
- `seaborn>=0.12.0` - Statistical visualization
- `scikit-learn>=1.3.0` - Machine learning utilities

## 🚀 Usage

### Starting the Dashboard
```bash
python acoustic_dashboard.py
```

The dashboard will be available at: `http://localhost:7860`

### Navigation
1. **Overview Tab**: View system status and pressure sensor data
2. **Acoustic Analysis**: Explore frequency spectrums and heatmaps
3. **Level Monitoring**: Monitor level sensor readings
4. **Technical Details**: Access comprehensive statistics and specifications

### Interactive Features
- **Time Slider**: Navigate through acoustic data samples
- **Sample Adjuster**: Modify heatmap resolution
- **Refresh Buttons**: Update visualizations with latest data
- **Responsive Layout**: Optimized for various screen sizes

## 🔬 Technical Specifications

### Acoustic Sensor Capabilities
- **Frequency Range**: 25Hz - 10kHz
- **Resolution**: 32-bit precision
- **Dynamic Range**: 120dB
- **Temporal Resolution**: 1 second intervals

### Pressure Sensor Specifications
- **Measurement Range**: 0-50,000 psi
- **Accuracy**: ±0.1% Full Scale
- **Response Time**: <10ms
- **Operating Temperature**: -40°C to +85°C

### Data Format
- **Timestamp**: ISO 8601 format (UTC)
- **Frequency Data**: 31 discrete frequency bands
- **Pressure Units**: PSI (Pounds per Square Inch)
- **Level Units**: Arbitrary units with relative scaling

## 📈 Data Visualization

### Plot Types
1. **Line Charts**: Time-series pressure and level data
2. **Spectrum Plots**: Frequency response analysis
3. **Heatmaps**: Temporal-frequency correlation
4. **Subplots**: Multi-parameter comparison views

### Interactive Elements
- **Zoom**: Pan and zoom capabilities
- **Hover**: Detailed data point information
- **Legend**: Toggle visibility of data series
- **Export**: Save plots as images

## 🎯 Use Cases

### Industrial Applications
- **Pipeline Monitoring**: Detect leaks and pressure anomalies
- **Equipment Health**: Monitor machinery vibration patterns
- **Process Control**: Real-time quality assurance
- **Predictive Maintenance**: Early warning systems

### Research & Development
- **Acoustic Analysis**: Frequency response characterization
- **Sensor Validation**: Performance benchmarking
- **Data Collection**: Large-scale monitoring studies
- **Algorithm Development**: Machine learning training data

## 🔧 Customization

### Adding New Sensors
1. Update the `load_data()` method in `AcousticSensorDashboard`
2. Add new visualization methods
3. Integrate with existing dashboard tabs

### Modifying Visualizations
1. Edit plot creation methods
2. Adjust color schemes and layouts
3. Add new interactive elements

### Data Processing
1. Implement real-time data streaming
2. Add data filtering and preprocessing
3. Integrate with external data sources

## 📝 File Structure

```
anomaly_detection/
├── acoustic_dashboard.py    # Main dashboard application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── data/                   # Sensor data files
│   ├── AC01-1400057.csv   # Acoustic sensor data
│   └── pressures.csv      # Pressure sensor data
└── docs/                   # Technical documentation
    └── acoustic_sensor.pdf # Sensor specifications
```

## 🚨 Troubleshooting

### Common Issues
1. **Data Loading Errors**: Check file paths and CSV format
2. **Memory Issues**: Reduce sample size in heatmap settings
3. **Plot Rendering**: Ensure all dependencies are installed
4. **Port Conflicts**: Change port number in launch parameters

### Performance Optimization
- Reduce data sample size for large datasets
- Use data sampling for real-time applications
- Implement data caching for repeated queries
- Optimize plot rendering with appropriate chart types

## 🤝 Contributing

### Development Guidelines
1. Follow Python PEP 8 style guidelines
2. Add comprehensive docstrings
3. Include error handling for robustness
4. Test with various data formats

### Feature Requests
- Submit detailed use case descriptions
- Include sample data formats
- Specify performance requirements
- Provide mockup designs if applicable

## 📄 License

This project is a proof-of-concept demonstration. Please contact the development team for licensing and commercial use inquiries.

## 📞 Support

For technical support, feature requests, or collaboration opportunities:
- **Project Team**: Acoustic Sensor Development Group
- **Documentation**: See `docs/acoustic_sensor.pdf` for detailed specifications
- **Data Format**: Refer to sample CSV files for data structure

---

**🎵 Revolutionizing Acoustic Sensing Technology** - This dashboard demonstrates the cutting-edge capabilities of next-generation acoustic sensors for industrial and research applications. 