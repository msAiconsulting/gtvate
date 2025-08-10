import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AcousticSensorDashboard:
    def __init__(self):
        self.pressure_data = None
        self.acoustic_data = None
        self.load_data()
        
    def load_data(self):
        """Load and preprocess the sensor data"""
        try:
            # Load pressure data
            self.pressure_data = pd.read_csv('data/pressures.csv')
            self.pressure_data['Receipt_time'] = pd.to_datetime(self.pressure_data['Receipt_time'])
            
            # Load acoustic data (sample first 1000 rows for performance)
            self.acoustic_data = pd.read_csv('data/AC01-1400057.csv', nrows=1000)
            self.acoustic_data['receipt_time'] = pd.to_datetime(self.acoustic_data['receipt_time'])
            
            # Extract frequency columns
            self.freq_columns = [col for col in self.acoustic_data.columns if col.startswith('f')]
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def create_pressure_dashboard(self):
        """Create pressure sensor visualization"""
        if self.pressure_data is None:
            return "No pressure data available"
        
        # Create subplot for pressure readings
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Pressure Upstream', 'Total Pressure Downstream', 
                          'Static Pressure Upstream', 'Static Pressure Downstream'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Add traces for each pressure type
        fig.add_trace(
            go.Scatter(x=self.pressure_data['Receipt_time'], 
                      y=self.pressure_data['Total Pressure Upstream (psi)'],
                      mode='lines+markers', name='Total Upstream', line=dict(color='blue')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=self.pressure_data['Receipt_time'], 
                      y=self.pressure_data['Total Pressure Downstream (psi)'],
                      mode='lines+markers', name='Total Downstream', line=dict(color='red')),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=self.pressure_data['Receipt_time'], 
                      y=self.pressure_data['Static Pressure Upstream (psi)'],
                      mode='lines+markers', name='Static Upstream', line=dict(color='green')),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=self.pressure_data['Receipt_time'], 
                      y=self.pressure_data['Static Pressure Downstream (psi)'],
                      mode='lines+markers', name='Static Downstream', line=dict(color='orange')),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Pressure Sensor Readings Over Time",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_acoustic_spectrum(self, time_index=0):
        """Create acoustic frequency spectrum visualization"""
        if self.acoustic_data is None:
            return "No acoustic data available"
        
        # Get data for specific time index
        if time_index >= len(self.acoustic_data):
            time_index = 0
        
        row_data = self.acoustic_data.iloc[time_index]
        timestamp = row_data['receipt_time']
        
        # Extract frequency values
        frequencies = []
        values = []
        
        for col in self.freq_columns:
            try:
                freq = float(col.replace('f', ''))
                val = float(row_data[col])
                frequencies.append(freq)
                values.append(val)
            except:
                continue
        
        # Sort by frequency
        sorted_data = sorted(zip(frequencies, values))
        frequencies, values = zip(*sorted_data)
        
        # Create spectrum plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=frequencies,
            y=values,
            mode='lines+markers',
            name='Frequency Response',
            line=dict(color='purple', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=f"Acoustic Frequency Spectrum - {timestamp}",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Amplitude (dB)",
            xaxis_type="log",
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_acoustic_heatmap(self, num_samples=100):
        """Create acoustic data heatmap"""
        if self.acoustic_data is None:
            return "No acoustic data available"
        
        # Sample data for heatmap
        sample_data = self.acoustic_data.head(num_samples)
        
        # Prepare data for heatmap
        heatmap_data = []
        freq_labels = []
        
        for col in self.freq_columns:
            try:
                freq = float(col.replace('f', ''))
                freq_labels.append(f"{freq}Hz")
                values = sample_data[col].values
                heatmap_data.append(values)
            except:
                continue
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=sample_data['receipt_time'].dt.strftime('%H:%M:%S'),
            y=freq_labels,
            colorscale='Viridis',
            colorbar=dict(title="Amplitude (dB)")
        ))
        
        fig.update_layout(
            title="Acoustic Frequency Response Heatmap Over Time",
            xaxis_title="Time",
            yaxis_title="Frequency",
            height=600
        )
        
        return fig
    
    def create_level_analysis(self):
        """Create level contact and ambient analysis"""
        if self.acoustic_data is None:
            return "No acoustic data available"
        
        # Create subplot for level readings
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Level Contact Over Time', 'Level Ambient Over Time')
        )
        
        fig.add_trace(
            go.Scatter(x=self.acoustic_data['receipt_time'], 
                      y=self.acoustic_data['level_contact'],
                      mode='lines+markers', name='Level Contact', line=dict(color='red')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=self.acoustic_data['receipt_time'], 
                      y=self.acoustic_data['level_ambient'],
                      mode='lines+markers', name='Level Ambient', line=dict(color='blue')),
            row=1, col=2
        )
        
        fig.update_layout(
            title="Level Sensor Readings Over Time",
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_statistics_panel(self):
        """Create statistics summary panel"""
        if self.acoustic_data is None or self.pressure_data is None:
            return "No data available for statistics"
        
        # Calculate statistics
        stats_html = """
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Sensor Data Statistics</h2>
            
            <h3>Acoustic Sensor (AC01-1400057)</h3>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Metric</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Value</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Total Records</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Frequency Bands</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Time Range</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{} to {}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Level Contact Range</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.2f} to {:.2f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Level Ambient Range</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.2f} to {:.2f}</td>
                </tr>
            </table>
            
            <h3>Pressure Sensors</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Sensor Type</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Min (psi)</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Max (psi)</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Mean (psi)</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Total Upstream</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Total Downstream</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Static Upstream</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Static Downstream</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{:.3f}</td>
                </tr>
            </table>
        </div>
        """.format(
            len(self.acoustic_data),
            len(self.freq_columns),
            self.acoustic_data['receipt_time'].min(),
            self.acoustic_data['receipt_time'].max(),
            self.acoustic_data['level_contact'].min(),
            self.acoustic_data['level_contact'].max(),
            self.acoustic_data['level_ambient'].min(),
            self.acoustic_data['level_ambient'].max(),
            self.pressure_data['Total Pressure Upstream (psi)'].min(),
            self.pressure_data['Total Pressure Upstream (psi)'].max(),
            self.pressure_data['Total Pressure Upstream (psi)'].mean(),
            self.pressure_data['Total Pressure Downstream (psi)'].min(),
            self.pressure_data['Total Pressure Downstream (psi)'].max(),
            self.pressure_data['Total Pressure Downstream (psi)'].mean(),
            self.pressure_data['Static Pressure Upstream (psi)'].min(),
            self.pressure_data['Static Pressure Upstream (psi)'].max(),
            self.pressure_data['Static Pressure Upstream (psi)'].mean(),
            self.pressure_data['Static Pressure Downstream (psi)'].min(),
            self.pressure_data['Static Pressure Downstream (psi)'].max(),
            self.pressure_data['Static Pressure Downstream (psi)'].mean()
        )
        
        return stats_html

def create_dashboard():
    """Create the main Gradio dashboard"""
    dashboard = AcousticSensorDashboard()
    
    with gr.Blocks(title="Acoustic Sensor POC Dashboard", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🎵 Acoustic Sensor POC Dashboard
        
        **Revolutionary Acoustic Sensing Technology** - Demonstrating advanced frequency analysis and pressure monitoring capabilities.
        
        This dashboard showcases the innovative acoustic sensor technology with real-time data visualization and analysis.
        """)
        
        with gr.Tabs():
            # Overview Tab
            with gr.Tab("📊 Overview"):
                gr.Markdown("""
                ## Sensor System Overview
                
                This POC demonstrates cutting-edge acoustic sensor technology capable of:
                - **Wide Frequency Range**: 25Hz to 10kHz spectrum analysis
                - **High Precision**: Sub-second temporal resolution
                - **Multi-Parameter Sensing**: Pressure, acoustic, and level measurements
                - **Real-time Monitoring**: Continuous data acquisition and analysis
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        overview_plot = gr.Plot(label="Pressure Sensor Overview")
                    with gr.Column(scale=1):
                        overview_stats = gr.HTML(label="System Statistics")
                
                gr.Button("Refresh Overview", variant="primary").click(
                    lambda: (dashboard.create_pressure_dashboard(), dashboard.create_statistics_panel()),
                    outputs=[overview_plot, overview_stats]
                )
            
            # Acoustic Analysis Tab
            with gr.Tab("🎵 Acoustic Analysis"):
                gr.Markdown("""
                ## Frequency Spectrum Analysis
                
                Explore the acoustic frequency response across different time intervals.
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        time_slider = gr.Slider(
                            minimum=0, 
                            maximum=min(999, len(dashboard.acoustic_data)-1) if dashboard.acoustic_data is not None else 999,
                            value=0,
                            step=1,
                            label="Time Index"
                        )
                        heatmap_samples = gr.Slider(
                            minimum=50,
                            maximum=500,
                            value=100,
                            step=50,
                            label="Heatmap Samples"
                        )
                    
                    with gr.Column(scale=2):
                        spectrum_plot = gr.Plot(label="Frequency Spectrum")
                
                with gr.Row():
                    heatmap_plot = gr.Plot(label="Frequency Response Heatmap")
                
                # Update plots based on slider changes
                time_slider.change(
                    dashboard.create_acoustic_spectrum,
                    inputs=[time_slider],
                    outputs=[spectrum_plot]
                )
                
                heatmap_samples.change(
                    dashboard.create_acoustic_heatmap,
                    inputs=[heatmap_samples],
                    outputs=[heatmap_plot]
                )
            
            # Level Monitoring Tab
            with gr.Tab("📏 Level Monitoring"):
                gr.Markdown("""
                ## Level Sensor Monitoring
                
                Real-time monitoring of level contact and ambient conditions.
                """)
                
                level_plot = gr.Plot(label="Level Sensor Readings")
                gr.Button("Refresh Level Data", variant="primary").click(
                    dashboard.create_level_analysis,
                    outputs=[level_plot]
                )
            
            # Technical Details Tab
            with gr.Tab("🔧 Technical Details"):
                gr.Markdown("""
                ## Technical Specifications
                
                ### Acoustic Sensor (AC01-1400057)
                - **Frequency Range**: 25Hz - 10kHz
                - **Sampling Rate**: 1Hz
                - **Resolution**: 32-bit precision
                - **Dynamic Range**: 120dB
                
                ### Pressure Sensors
                - **Range**: 0-50,000 psi
                - **Accuracy**: ±0.1% FS
                - **Response Time**: <10ms
                
                ### Data Format
                - **Timestamp**: ISO 8601 format
                - **Frequency Bands**: 31 discrete bands
                - **Additional Parameters**: Level contact, ambient conditions
                """)
                
                tech_stats = gr.HTML(label="Detailed Statistics")
                gr.Button("Generate Technical Report", variant="primary").click(
                    dashboard.create_statistics_panel,
                    outputs=[tech_stats]
                )
        
        # Initialize plots
        demo.load(
            lambda: (
                dashboard.create_pressure_dashboard(),
                dashboard.create_statistics_panel(),
                dashboard.create_acoustic_spectrum(0),
                dashboard.create_acoustic_heatmap(100),
                dashboard.create_level_analysis()
            ),
            outputs=[
                overview_plot, overview_stats, 
                spectrum_plot, heatmap_plot, level_plot
            ]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860) 