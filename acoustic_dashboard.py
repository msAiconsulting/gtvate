import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import threading
from datetime import datetime, timedelta
import random

class AcousticSensorDashboard:
    def __init__(self):
        self.load_data()
        self.simulation_running = False
        self.simulation_thread = None
        self.current_time_index = 0
        self.simulation_data = []
        self.simulation_start_time = None
        
    def load_data(self):
        """Load sensor data from CSV files"""
        try:
            # Load pressure data
            self.pressure_data = pd.read_csv('data/pressures.csv')
            self.pressure_data['Receipt_time'] = pd.to_datetime(self.pressure_data['Receipt_time'])
            
            # Load acoustic data (first 1000 rows for performance)
            self.acoustic_data = pd.read_csv('data/AC01-1400057.csv', nrows=1000)
            self.acoustic_data['receipt_time'] = pd.to_datetime(self.acoustic_data['receipt_time'])
            
            # Get frequency columns
            self.freq_columns = [col for col in self.acoustic_data.columns if col.startswith('f')]
            
            print(f"✅ Data loaded: {len(self.pressure_data)} pressure records, {len(self.acoustic_data)} acoustic records")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.pressure_data = None
            self.acoustic_data = None
            self.freq_columns = []

    def generate_simulation_data(self, duration_minutes=10, update_interval=1):
        """Generate realistic simulation data based on actual sensor patterns"""
        if not self.acoustic_data.empty:
            # Use actual data patterns as base
            base_freq_data = self.acoustic_data[self.freq_columns].iloc[0].values
            base_levels = self.acoustic_data[['level_contact', 'level_ambient']].iloc[0].values
            
            # Generate time points
            start_time = datetime.now()
            time_points = []
            freq_data = []
            level_data = []
            pressure_data = []
            
            # Ensure integer values for range function
            total_seconds = int(duration_minutes * 60)
            interval_seconds = max(1, int(update_interval))  # Ensure minimum interval of 1 second
            for i in range(0, total_seconds, interval_seconds):
                current_time = start_time + timedelta(seconds=i * update_interval)
                time_points.append(current_time)
                
                # Add realistic variations to frequency data
                noise = np.random.normal(0, 0.5, len(base_freq_data))
                trend = np.sin(2 * np.pi * i / (60 * 10)) * 2  # 10-minute cycle
                new_freq = base_freq_data + noise + trend
                freq_data.append(new_freq)
                
                # Add variations to level data
                level_noise = np.random.normal(0, 10, 2)
                level_trend = np.sin(2 * np.pi * i / (60 * 5)) * 20  # 5-minute cycle
                new_levels = base_levels + level_noise + level_trend
                level_data.append(new_levels)
                
                # Generate pressure variations
                base_pressure = 1.0
                pressure_noise = np.random.normal(0, 0.1)
                pressure_trend = np.sin(2 * np.pi * i / (60 * 3)) * 0.3  # 3-minute cycle
                new_pressure = base_pressure + pressure_noise + pressure_trend
                pressure_data.append([new_pressure, new_pressure * 0.95, 0.26, 0.08])
            
            return {
                'time_points': time_points,
                'freq_data': np.array(freq_data),
                'level_data': np.array(level_data),
                'pressure_data': np.array(pressure_data)
            }
        return None

    def start_simulation(self, duration_minutes, update_interval):
        """Start the real-time simulation"""
        if self.simulation_running:
            return "Simulation already running!"
        
        self.simulation_running = True
        self.simulation_data = self.generate_simulation_data(duration_minutes, update_interval)
        self.simulation_start_time = datetime.now()
        self.current_time_index = 0
        
        # Start simulation thread
        self.simulation_thread = threading.Thread(
            target=self._simulation_loop,
            args=(duration_minutes, update_interval)
        )
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        
        return f"🚀 Simulation started! Running for {duration_minutes} minutes with {update_interval}s updates."

    def stop_simulation(self):
        """Stop the simulation"""
        self.simulation_running = False
        if self.simulation_thread:
            self.simulation_thread.join(timeout=1)
        return "⏹️ Simulation stopped."

    def _simulation_loop(self, duration_minutes, update_interval):
        """Main simulation loop"""
        # Ensure update_interval is a positive number
        interval = max(0.1, float(update_interval))
        while self.simulation_running and self.current_time_index < len(self.simulation_data['time_points']):
            time.sleep(interval)
            self.current_time_index += 1

    def get_simulation_status(self):
        """Get current simulation status"""
        if not self.simulation_running:
            return "⏸️ Simulation not running"
        
        elapsed = datetime.now() - self.simulation_start_time
        progress = (self.current_time_index / len(self.simulation_data['time_points'])) * 100 if self.simulation_data else 0
        
        # Convert timedelta to minutes and seconds for display
        elapsed_minutes = int(elapsed.total_seconds() // 60)
        elapsed_seconds = int(elapsed.total_seconds() % 60)
        
        return f"🔄 LIVE - Elapsed: {elapsed_minutes:02d}:{elapsed_seconds:02d} | Progress: {progress:.1f}% | Data Points: {self.current_time_index + 1}"

    def create_real_time_pressure_dashboard(self):
        """Create real-time pressure monitoring dashboard"""
        if not self.simulation_running or self.simulation_data is None:
            return self.create_pressure_dashboard()
        
        # Get current simulation data
        current_data = self.simulation_data['pressure_data'][:self.current_time_index + 1]
        time_points = self.simulation_data['time_points'][:self.current_time_index + 1]
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Total Pressure (Real-time)', 'Static Pressure (Real-time)'),
            vertical_spacing=0.1
        )
        
        # Total pressure
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=current_data[:, 0],
                name='Upstream',
                line=dict(color='blue', width=2),
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=current_data[:, 1],
                name='Downstream',
                line=dict(color='red', width=2),
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        # Static pressure
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=current_data[:, 2],
                name='Static Downstream',
                line=dict(color='green', width=2),
                mode='lines+markers'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=current_data[:, 3],
                name='Static Upstream',
                line=dict(color='orange', width=2),
                mode='lines+markers'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'Real-time Pressure Monitoring - {self.current_time_index + 1} data points',
            height=600,
            showlegend=True,
            xaxis_title='Time',
            yaxis_title='Pressure (psi)'
        )
        
        # Add real-time indicator
        if self.simulation_running:
            fig.add_annotation(
                x=time_points[-1] if time_points else datetime.now(),
                y=current_data[-1, 0] if len(current_data) > 0 else 0,
                text="🔄 LIVE",
                showarrow=True,
                arrowhead=2,
                arrowcolor="red",
                arrowwidth=2,
                arrowsize=1,
                bgcolor="yellow",
                bordercolor="red",
                borderwidth=2
            )
        
        return fig

    def create_real_time_acoustic_spectrum(self, time_index=None):
        """Create real-time acoustic spectrum visualization"""
        if not self.simulation_running or self.simulation_data is None:
            return self.create_acoustic_spectrum(0)
        
        if time_index is None:
            time_index = self.current_time_index
        
        if time_index >= len(self.simulation_data['freq_data']):
            time_index = len(self.simulation_data['freq_data']) - 1
        
        # Get frequency data for current time
        freq_values = self.simulation_data['freq_data'][time_index]
        freq_labels = self.freq_columns
        
        # Create spectrum plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=freq_labels,
            y=freq_values,
            mode='lines+markers',
            name=f'Time: {self.simulation_data["time_points"][time_index].strftime("%H:%M:%S")}',
            line=dict(color='purple', width=3),
            marker=dict(size=8, color='purple')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Real-time Acoustic Spectrum - {self.simulation_data["time_points"][time_index].strftime("%H:%M:%S")}',
            xaxis_title='Frequency (Hz)',
            yaxis_title='Amplitude (dB)',
            height=500,
            showlegend=True
        )
        
        # Set x-axis to log scale
        fig.update_xaxes(type='log')
        
        return fig

    def create_real_time_acoustic_heatmap(self, num_samples=None):
        """Create real-time acoustic heatmap"""
        if not self.simulation_running or self.simulation_data is None:
            return self.create_acoustic_heatmap(50)
        
        if num_samples is None:
            num_samples = min(self.current_time_index + 1, 100)
        
        # Get recent frequency data
        recent_freq_data = self.simulation_data['freq_data'][:num_samples]
        time_labels = [t.strftime("%H:%M:%S") for t in self.simulation_data['time_points'][:num_samples]]
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=recent_freq_data.T,
            x=time_labels,
            y=self.freq_columns,
            colorscale='Viridis',
            colorbar=dict(title='Amplitude (dB)')
        ))
        
        fig.update_layout(
            title=f'Real-time Acoustic Frequency Response - Last {num_samples} samples',
            xaxis_title='Time',
            yaxis_title='Frequency (Hz)',
            height=600
        )
        
        return fig

    def create_real_time_level_analysis(self):
        """Create real-time level monitoring"""
        if not self.simulation_running or self.simulation_data is None:
            return self.create_level_analysis()
        
        # Get current level data
        current_data = self.simulation_data['level_data'][:self.current_time_index + 1]
        time_points = self.simulation_data['time_points'][:self.current_time_index + 1]
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Level Contact (Real-time)', 'Level Ambient (Real-time)'),
            vertical_spacing=0.1
        )
        
        # Level contact
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=current_data[:, 0],
                name='Level Contact',
                line=dict(color='blue', width=2),
                mode='lines+markers',
                fill='tonexty'
            ),
            row=1, col=1
        )
        
        # Level ambient
        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=current_data[:, 1],
                name='Level Ambient',
                line=dict(color='green', width=2),
                mode='lines+markers',
                fill='tonexty'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'Real-time Level Monitoring - {self.current_time_index + 1} data points',
            height=600,
            showlegend=True,
            xaxis_title='Time',
            yaxis_title='Level'
        )
        
        return fig

    def create_pressure_dashboard(self):
        """Create pressure monitoring dashboard"""
        if self.pressure_data is None:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Total Pressure', 'Static Pressure'),
            vertical_spacing=0.1
        )
        
        # Total pressure
        fig.add_trace(
            go.Scatter(
                x=self.pressure_data['Receipt_time'],
                y=self.pressure_data['Total Pressure Upstream (psi)'],
                name='Upstream',
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.pressure_data['Receipt_time'],
                y=self.pressure_data['Total Pressure Downstream (psi)'],
                name='Downstream',
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        # Static pressure
        fig.add_trace(
            go.Scatter(
                x=self.pressure_data['Receipt_time'],
                y=self.pressure_data['Static Pressure Downstream (psi)'],
                name='Static Downstream',
                mode='lines+markers'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.pressure_data['Receipt_time'],
                y=self.pressure_data['Static Pressure Upstream (psi)'],
                name='Static Upstream',
                mode='lines+markers'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title='Pressure Sensor Monitoring',
            height=600,
            showlegend=True
        )
        
        return fig

    def create_acoustic_spectrum(self, time_index):
        """Create acoustic spectrum visualization"""
        if self.acoustic_data is None or time_index >= len(self.acoustic_data):
            return go.Figure()
        
        freq_values = self.acoustic_data[self.freq_columns].iloc[time_index].values
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.freq_columns,
            y=freq_values,
            mode='lines+markers',
            name=f'Time: {self.acoustic_data["receipt_time"].iloc[time_index].strftime("%H:%M:%S")}'
        ))
        
        fig.update_layout(
            title='Acoustic Frequency Spectrum',
            xaxis_title='Frequency (Hz)',
            yaxis_title='Amplitude (dB)',
            height=500
        )
        
        fig.update_xaxes(type='log')
        
        return fig

    def create_acoustic_heatmap(self, num_samples):
        """Create acoustic heatmap visualization"""
        if self.acoustic_data is None:
            return go.Figure()
        
        # Use the specified number of samples
        sample_data = self.acoustic_data.head(num_samples)
        freq_data = sample_data[self.freq_columns].values.T
        
        time_labels = [t.strftime("%H:%M:%S") for t in sample_data['receipt_time']]
        
        fig = go.Figure(data=go.Heatmap(
            z=freq_data,
            x=time_labels,
            y=self.freq_columns,
            colorscale='Viridis',
            colorbar=dict(title='Amplitude (dB)')
        ))
        
        fig.update_layout(
            title=f'Acoustic Frequency Response Over Time ({num_samples} samples)',
            xaxis_title='Time',
            yaxis_title='Frequency (Hz)',
            height=600
        )
        
        return fig

    def create_level_analysis(self):
        """Create level monitoring visualization"""
        if self.acoustic_data is None:
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Level Contact', 'Level Ambient'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.acoustic_data['receipt_time'],
                y=self.acoustic_data['level_contact'],
                name='Level Contact',
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.acoustic_data['receipt_time'],
                y=self.acoustic_data['level_ambient'],
                name='Level Ambient',
                mode='lines+markers'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title='Level Sensor Monitoring',
            height=600,
            showlegend=True
        )
        
        return fig

    def create_statistics_panel(self):
        """Create statistics summary panel"""
        if self.acoustic_data is None or self.pressure_data is None:
            return "Data not available"
        
        # Calculate statistics
        acoustic_stats = {
            'Total Records': len(self.acoustic_data),
            'Frequency Bands': len(self.freq_columns),
            'Frequency Range': f"{self.freq_columns[0]} - {self.freq_columns[-1]}",
            'Level Contact Range': f"{self.acoustic_data['level_contact'].min():.1f} - {self.acoustic_data['level_contact'].max():.1f}",
            'Level Ambient Range': f"{self.acoustic_data['level_ambient'].min():.1f} - {self.acoustic_data['level_ambient'].max():.1f}"
        }
        
        pressure_stats = {
            'Total Records': len(self.pressure_data),
            'Pressure Range': f"{self.pressure_data['Total Pressure Upstream (psi)'].min():.3f} - {self.pressure_data['Total Pressure Upstream (psi)'].max():.3f} psi",
            'Data Period': f"{self.pressure_data['Receipt_time'].min().strftime('%Y-%m-%d %H:%M')} to {self.pressure_data['Receipt_time'].max().strftime('%Y-%m-%d %H:%M')}"
        }
        
        # Create HTML summary
        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2E86AB;">📊 Sensor Data Statistics</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #2E86AB;">
                    <h3 style="color: #2E86AB; margin-top: 0;">🎵 Acoustic Sensor (AC01-1400057)</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>📈 <strong>Total Records:</strong> {acoustic_stats['Total Records']:,}</li>
                        <li>🎚️ <strong>Frequency Bands:</strong> {acoustic_stats['Frequency Bands']}</li>
                        <li>🔊 <strong>Frequency Range:</strong> {acoustic_stats['Frequency Range']}</li>
                        <li>📏 <strong>Level Contact:</strong> {acoustic_stats['Level Contact Range']}</li>
                        <li>🌡️ <strong>Level Ambient:</strong> {acoustic_stats['Level Ambient Range']}</li>
                    </ul>
                </div>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                    <h3 style="color: #28a745; margin-top: 0;">📊 Pressure Sensors</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>📈 <strong>Total Records:</strong> {pressure_stats['Total Records']:,}</li>
                        <li>⚡ <strong>Pressure Range:</strong> {pressure_stats['Pressure Range']}</li>
                        <li>🕒 <strong>Data Period:</strong> {pressure_stats['Data Period']}</li>
                        <li>🎯 <strong>Accuracy:</strong> ±0.1% Full Scale</li>
                        <li>⚡ <strong>Response Time:</strong> <10ms</li>
                    </ul>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
                <h3 style="color: #2196f3; margin-top: 0;">🚀 Real-time Simulation</h3>
                <p style="margin: 0; color: #1976d2;">
                    The dashboard now includes real-time time series simulation capabilities, 
                    allowing you to demonstrate live sensor data visualization and monitoring.
                </p>
            </div>
        </div>
        """
        
        return html_content

def create_dashboard():
    """Create the Gradio dashboard interface"""
    dashboard = AcousticSensorDashboard()
    
    with gr.Blocks(
        title="🎵 Acoustic Sensor POC Dashboard - Real-time Simulation",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        .status-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
            font-weight: bold;
        }
        """
    ) as demo:
        gr.Markdown("""
        # 🎵 Acoustic Sensor POC Dashboard
        ## Revolutionary Acoustic Sensing Technology with Real-time Simulation
        
        This dashboard showcases cutting-edge acoustic sensor capabilities through interactive visualizations and live time series simulation.
        """)
        
        # Simulation Control Panel
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 🚀 Real-time Simulation Controls")
                with gr.Row():
                    duration_slider = gr.Slider(
                        minimum=1, maximum=30, value=10, step=1,
                        label="Simulation Duration (minutes)"
                    )
                    interval_slider = gr.Slider(
                        minimum=0.5, maximum=5, value=1, step=0.5,
                        label="Update Interval (seconds)"
                    )
                
                with gr.Row():
                    start_btn = gr.Button("🚀 Start Simulation", variant="primary")
                    stop_btn = gr.Button("⏹️ Stop Simulation", variant="stop")
                    refresh_btn = gr.Button("🔄 Refresh All", variant="secondary")
                
                status_display = gr.HTML(
                    value="⏸️ Simulation not running",
                    elem_classes=["status-box"]
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Live Status")
                live_status = gr.HTML(
                    value="Ready to start simulation...",
                    elem_classes=["status-box"]
                )
        
        # Main Dashboard Tabs
        with gr.Tabs():
            # Overview Tab
            with gr.Tab("📊 Overview - Real-time"):
                gr.Markdown("### 🔄 Live Pressure Monitoring")
                pressure_plot = gr.Plot(
                    value=dashboard.create_pressure_dashboard(),
                    label="Pressure Dashboard"
                )
                
                gr.Markdown("### 📈 System Statistics")
                stats_panel = gr.HTML(
                    value=dashboard.create_statistics_panel(),
                    label="Statistics"
                )
            
            # Acoustic Analysis Tab
            with gr.Tab("🎵 Acoustic Analysis - Real-time"):
                gr.Markdown("### 🎵 Live Frequency Spectrum")
                with gr.Row():
                    time_slider = gr.Slider(
                        minimum=0, maximum=999, value=0, step=1,
                        label="Time Index (for historical data)"
                    )
                    sample_slider = gr.Slider(
                        minimum=50, maximum=500, value=100, step=50,
                        label="Heatmap Samples"
                    )
                
                spectrum_plot = gr.Plot(
                    value=dashboard.create_acoustic_spectrum(0),
                    label="Acoustic Spectrum"
                )
                
                gr.Markdown("### 🔥 Live Frequency Heatmap")
                heatmap_plot = gr.Plot(
                    value=dashboard.create_acoustic_heatmap(100),
                    label="Acoustic Heatmap"
                )
            
            # Level Monitoring Tab
            with gr.Tab("📏 Level Monitoring - Real-time"):
                gr.Markdown("### 📏 Live Level Monitoring")
                level_plot = gr.Plot(
                    value=dashboard.create_level_analysis(),
                    label="Level Analysis"
                )
            
            # Technical Details Tab
            with gr.Tab("🔧 Technical Details"):
                gr.Markdown("### 📋 Sensor Specifications")
                gr.Markdown("""
                ## 🎵 Acoustic Sensor (AC01-1400057)
                
                **Frequency Range**: 25Hz to 10kHz (27 discrete bands)  
                **Dynamic Range**: 120dB  
                **Resolution**: 32-bit  
                **Temporal Resolution**: 1 second  
                **Applications**: Industrial monitoring, research, quality control
                
                ## 📊 Pressure Sensors
                
                **Measurement Range**: 0-50,000 PSI  
                **Accuracy**: ±0.1% Full Scale  
                **Response Time**: <10ms  
                **Applications**: Pipeline monitoring, process control, safety systems
                
                ## 🚀 Real-time Simulation Features
                
                **Live Data Generation**: Realistic sensor data patterns  
                **Time Series Animation**: Continuous data flow visualization  
                **Interactive Controls**: Adjustable simulation parameters  
                **Performance Monitoring**: Real-time status and progress tracking  
                **Multi-sensor Integration**: Coordinated data visualization
                """)
        
        # Event handlers
        def start_sim(duration, interval):
            result = dashboard.start_simulation(duration, interval)
            return result, dashboard.get_simulation_status()
        
        def stop_sim():
            result = dashboard.stop_simulation()
            return result, "⏸️ Simulation stopped"
        
        def refresh_all():
            return (
                dashboard.create_real_time_pressure_dashboard(),
                dashboard.create_real_time_acoustic_spectrum(),
                dashboard.create_real_time_acoustic_heatmap(),
                dashboard.create_real_time_level_analysis(),
                dashboard.get_simulation_status()
            )
        
        def update_live_status():
            return dashboard.get_simulation_status()
        
        # Connect event handlers
        start_btn.click(
            start_sim,
            inputs=[duration_slider, interval_slider],
            outputs=[status_display, live_status]
        )
        
        stop_btn.click(
            stop_sim,
            outputs=[status_display, live_status]
        )
        
        refresh_btn.click(
            refresh_all,
            outputs=[pressure_plot, spectrum_plot, heatmap_plot, level_plot, live_status]
        )
        
        # Auto-refresh for live status
        demo.load(update_live_status, outputs=[live_status])
        
        # Update plots based on simulation state
        time_slider.change(
            lambda x: dashboard.create_real_time_acoustic_spectrum(x) if dashboard.simulation_running else dashboard.create_acoustic_spectrum(x),
            inputs=[time_slider],
            outputs=[spectrum_plot]
        )
        
        sample_slider.change(
            lambda x: dashboard.create_real_time_acoustic_heatmap(x) if dashboard.simulation_running else dashboard.create_acoustic_heatmap(x),
            inputs=[sample_slider],
            outputs=[heatmap_plot]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 