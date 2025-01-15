import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ai_agents import get_all_agents
import numpy as np

st.set_page_config(page_title="AI Integration Analysis", layout="wide")

# Initialize session state
if 'investment_level' not in st.session_state:
    st.session_state.investment_level = 1.0
if 'public_trust' not in st.session_state:
    st.session_state.public_trust = 1.0

def create_timeline(agents):
    df = pd.DataFrame([
        {
            'Agent': agent.name.replace(' Agent', ''),  # Remove 'Agent' suffix for cleaner display
            'Start Year': 2025,
            'Integration Year': agent.integration_year,
            'Domain': agent.domain,
            'Description': agent.description
        }
        for agent in agents
    ])
    
    fig = px.timeline(
        df.sort_values('Integration Year'),
        x_start='Start Year',
        x_end='Integration Year',
        y='Agent',
        color='Domain',
        title='Predicted AI Integration Timeline (2025-2035)',
        labels={'Integration Year': 'Year', 'Agent': 'Sector'},
        hover_data=['Description']  # Show description on hover
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis=dict(
            type='linear',
            range=[2024.5, 2035.5],  # Extend range slightly for better visibility
            dtick=1,  # Show every year
            tickformat='d',  # Format as decimal years
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        plot_bgcolor='rgba(0,0,0,0.05)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        title_font_size=20,
        height=400,  # Fixed height for better proportions
        margin=dict(l=10, r=10, t=50, b=10),  # Adjust margins
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.1)',
            font=dict(size=12)
        )
    )
    
    # Add vertical line for current year with annotation
    fig.add_vline(
        x=2025, 
        line_dash="dash", 
        line_color="yellow",
        annotation_text="Present (2025)",
        annotation_position="top",
        annotation_font_size=12,
        annotation_font_color="yellow"
    )
    
    # Customize hover template
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
                     "Start: %{x_start}<br>" +
                     "Complete: %{x_end}<br>" +
                     "Domain: %{color}<br>" +
                     "<i>%{customdata[0]}</i><extra></extra>"
    )
    
    return fig

def create_predictions_chart(agents):
    years = list(range(2025, 2035))
    data = []
    
    for agent in agents:
        base_year = agent.integration_year
        progress = []
        for year in years:
            if year >= 2025:
                if year >= base_year:
                    progress.append(100)
                else:
                    # Calculate progress as a percentage
                    progress.append(((year - 2025) / (base_year - 2025)) * 100)
        data.append(go.Scatter(
            x=years,
            y=progress,
            name=agent.name,
            mode='lines+markers'
        ))
    
    fig = go.Figure(data=data)
    fig.update_layout(
        title='AI Integration Progress Over Time',
        xaxis_title='Year',
        yaxis_title='Integration Progress (%)',
        yaxis_range=[0, 100]
    )
    return fig

def create_blueprint_timeline():
    # Create data for the timeline
    phases = {
        "Phase 1: Foundation": [
            ("2025 Q1", "OpenAI-US Government Partnership Kickoff (Jan 30)"),
            ("2025 Q2", "Launch of National AI Research Centers"),
            ("2025 Q3", "Implementation of AI Safety Guidelines"),
            ("2025 Q4", "Establishment of AI Economic Zones"),
            ("2026 Q1", "Roll-out of AI Education Initiative"),
            ("2026 Q2", "Public-Private AI Infrastructure Partnership"),
            ("2026 Q4", "First Wave of AI Industry Standards"),
            ("2027 Q2", "Completion of Initial AI Safety Framework")
        ],
        "Phase 2: Acceleration": [
            ("2027 Q3", "Launch of AI Workforce Transition Program"),
            ("2027 Q4", "Implementation of Cross-Border AI Collaboration"),
            ("2028 Q1", "Deployment of AI-Enhanced Public Services"),
            ("2028 Q3", "Establishment of AI Innovation Hubs"),
            ("2028 Q4", "Roll-out of National AI Infrastructure"),
            ("2029 Q2", "Integration of AI in Critical Industries")
        ],
        "Phase 3: Maturation": [
            ("2029 Q3", "Achievement of AI Education Milestones"),
            ("2029 Q4", "Full Implementation of AI Safety Standards"),
            ("2030 Q1", "Completion of AI Economic Zone Network"),
            ("2030 Q3", "Establishment of Global AI Partnership"),
            ("2030 Q4", "Launch of Advanced AI Research Initiatives"),
            ("2031 Q2", "Achievement of Full AI Integration Goals"),
            ("2032 Q1", "Global AI Governance Framework"),
            ("2032 Q4", "Advanced AI-Human Collaboration Systems"),
            ("2033 Q2", "Universal AI Education Achievement"),
            ("2034 Q1", "Quantum-AI Integration Milestone"),
            ("2034 Q4", "Sustainable AI Infrastructure Complete"),
            ("2035 Q2", "Full Societal AI Integration Achieved")
        ]
    }
    
    # Convert dates to numerical values for plotting
    def date_to_num(date_str):
        year = int(date_str.split()[0])
        quarter = int(date_str.split()[1][1])
        return year + (quarter - 1) * 0.25

    # Create DataFrame for plotting with waterfall offsets
    data = []
    colors = ['rgb(70, 130, 180)', 'rgb(30, 144, 255)', 'rgb(34, 139, 34)']
    
    # Calculate offsets for waterfall effect
    def get_y_offset(index, total):
        if total <= 1:
            return 0
        max_offset = 0.4  # Maximum offset from the center
        if index % 2 == 0:
            return -max_offset * (index / (total - 1))
        else:
            return max_offset * ((index + 1) / (total - 1))

    for i, (phase, milestones) in enumerate(phases.items()):
        for j, (date, milestone) in enumerate(milestones):
            offset = get_y_offset(j, len(milestones))
            data.append({
                'Phase': phase,
                'Date': date,
                'Milestone': milestone,
                'DateNum': date_to_num(date),
                'Color': colors[i],
                'YOffset': offset
            })
    
    df = pd.DataFrame(data)
    
    # Create the figure
    fig = go.Figure()
    
    # Add phase background rectangles
    phase_ranges = {
        "Phase 1: Foundation": (2025, 2027.5),
        "Phase 2: Acceleration": (2027.5, 2029.5),
        "Phase 3: Maturation": (2029.5, 2031.5)
    }
    
    for phase, (start, end) in phase_ranges.items():
        fig.add_shape(
            type="rect",
            x0=start,
            x1=end,
            y0=-0.8,
            y1=0.8,
            fillcolor="rgba(128, 128, 128, 0.1)",
            line=dict(width=0),
            layer="below"
        )
    
    # Add milestone markers with waterfall effect
    for phase in phases.keys():
        phase_data = df[df['Phase'] == phase]
        base_y = list(phases.keys()).index(phase)
        
        fig.add_trace(go.Scatter(
            x=phase_data['DateNum'],
            y=[base_y + offset for offset in phase_data['YOffset']],
            mode='markers+text',
            name=phase,
            text=phase_data['Milestone'],
            textposition="top center",
            textfont=dict(size=11),
            marker=dict(
                size=12,
                color=phase_data['Color'].iloc[0],
                symbol='diamond',
                line=dict(color='white', width=1)
            ),
            hovertemplate="<b>%{text}</b><br>" +
                         "Date: %{customdata}<extra></extra>",
            customdata=phase_data['Date']
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="OpenAI Economic Blueprint Timeline",
            font=dict(size=24, color='white'),
            x=0.5,
            y=0.95
        ),
        showlegend=True,
        height=600,  # Increased height for better spacing
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211,211,211,0.2)',
            ticktext=list(phases.keys()),
            tickvals=list(range(len(phases))),
            title=None,
            tickfont=dict(size=14),
            range=[-0.8, 2.8]  # Adjusted range for waterfall effect
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211,211,211,0.2)',
            ticktext=['2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035'],
            tickvals=[2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035],
            title="Year",
            titlefont=dict(size=16),
            tickfont=dict(size=12),
            range=[2024.8, 2035.2]
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.3)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(size=12)
        ),
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Add vertical line for current date
    fig.add_vline(
        x=2025,
        line_dash="dash",
        line_color="yellow",
        line_width=2,
        annotation_text="Present (2025)",
        annotation_position="top",
        annotation_font_size=14,
        annotation_font_color="yellow"
    )
    
    # Add phase labels
    for phase, (start, end) in phase_ranges.items():
        fig.add_annotation(
            x=(start + end) / 2,
            y=2.7,
            text=phase.split(":")[0],
            showarrow=False,
            font=dict(size=14, color="white"),
            opacity=0.7
        )
    
    return fig

def display_agent_details(agents):
    for agent in agents:
        st.subheader(f"{agent.name} - Integration Year: {agent.integration_year}")
        st.markdown(f"""
        **Domain:** {agent.domain}
        
        **Description:** {agent.description}
        
        **Yearly Milestones:**
        """)
        
        # Create a clean table-like display for milestones
        for year, milestone in agent.yearly_milestones.items():
            st.markdown(f"- **{year}:** {milestone}")
        
        st.markdown("\n**Key Predictions:**")
        for i, pred in enumerate(agent.predictions, 1):
            st.markdown(f"{i}. {pred}")
        
        st.markdown("---")  # Add separator between agents

def generate_comparison_report():
    report_content = """# AI Integration Approaches Comparison Report

## Executive Summary
This report compares two distinct approaches to AI integration in America:
1. AI Agents' Independent Analysis
2. OpenAI-US Government Blueprint

## Approach Comparison

### Timeline and Pacing
* **AI Agents**
  - Sector-specific integration timelines
  - Varying completion dates based on domain complexity
  - Focus on technological readiness

* **OpenAI-Gov**
  - Structured three-phase approach
  - Synchronized milestones across sectors
  - Coordinated implementation schedule

### Integration Strategy
* **AI Agents**
  - Bottom-up approach
  - Focus on technological readiness
  - Domain-specific implementation
  - Adaptive to sector needs

* **OpenAI-Gov**
  - Top-down approach
  - Policy-driven framework
  - Standardized implementation
  - Coordinated across sectors

### Priority Areas
* **AI Agents**
  - Practical implementation
  - Domain expertise
  - Technical capabilities
  - Sector-specific solutions

* **OpenAI-Gov**
  - Infrastructure development
  - Governance frameworks
  - Standardization
  - Cross-sector coordination

### Risk Management
* **AI Agents**
  - Domain-specific risk assessment
  - Targeted mitigation strategies
  - Focus on technical safety
  - Adaptive risk management

* **OpenAI-Gov**
  - Comprehensive safety framework
  - Phased deployment
  - Regulatory oversight
  - Standardized safety protocols

## Areas of Agreement
Both approaches recognize the need for:
- Strong safety guidelines and ethical considerations
- Public-private partnerships
- Education and workforce development
- Global collaboration
- Phased implementation
- Regular assessment and adaptation

## Notable Insights
1. The AI Agents' approach provides more granular, sector-specific insights
2. The OpenAI-Gov blueprint offers a more coordinated, policy-driven framework
3. Both timelines converge on full integration around 2035
4. Complementary strengths in different areas

## Recommendations
1. Consider integrating elements from both approaches
2. Leverage AI Agents' domain expertise within the policy framework
3. Maintain flexibility while ensuring coordination
4. Regular assessment and alignment of both approaches

## Conclusion
While the approaches differ in methodology and focus, they are complementary rather than contradictory. A successful AI integration strategy might combine the structured policy framework of the OpenAI-Gov approach with the domain-specific insights of the AI Agents' analysis.
"""
    return report_content.encode('utf-8')

def create_milestone_heatmap(agents):
    # Create data for milestone density
    years = range(2025, 2036)
    data = []
    
    for agent in agents:
        row = []
        for year in years:
            # Count milestones per year
            count = sum(1 for y in agent.yearly_milestones.keys() if y == year)
            row.append(count)
        data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=list(years),
        y=[agent.name.split(' Agent')[0] for agent in agents],
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate='Year: %{x}<br>Domain: %{y}<br>Milestones: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Milestone Density by Domain and Year',
        xaxis_title='Year',
        yaxis_title='Domain',
        height=400,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_domain_relationships(agents):
    # Create relationship matrix based on shared milestones timing
    n = len(agents)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                # Calculate relationship strength based on milestone proximity
                strength = 0
                for year_i in agents[i].yearly_milestones.keys():
                    for year_j in agents[j].yearly_milestones.keys():
                        if abs(year_i - year_j) <= 1:  # Related if milestones within 1 year
                            strength += 1
                matrix[i][j] = strength
    
    # Create network graph
    edge_x = []
    edge_y = []
    edge_weights = []
    
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] > 0:
                angle_i = 2 * np.pi * i / n
                angle_j = 2 * np.pi * j / n
                radius = 1
                
                x0 = radius * np.cos(angle_i)
                y0 = radius * np.sin(angle_i)
                x1 = radius * np.cos(angle_j)
                y1 = radius * np.sin(angle_j)
                
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_weights.append(matrix[i][j])
    
    edges_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='rgba(255,255,255,0.3)'),
        hoverinfo='none',
        mode='lines'
    )
    
    node_x = [radius * np.cos(2 * np.pi * i / n) for i in range(n)]
    node_y = [radius * np.sin(2 * np.pi * i / n) for i in range(n)]
    
    nodes_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[agent.name.split(' Agent')[0] for agent in agents],
        textposition="middle center",
        marker=dict(
            size=20,
            color=['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)',
                   'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                   'rgb(227, 119, 194)'][:n],
            line=dict(color='white', width=1)
        )
    )
    
    fig = go.Figure(data=[edges_trace, nodes_trace])
    
    fig.update_layout(
        title='Domain Integration Relationships',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_integration_progress_chart(agents):
    # Create data for cumulative progress
    years = np.arange(2025, 2036, 0.25)  # Quarterly progress
    domains = [agent.name.split(' Agent')[0] for agent in agents]
    
    # Calculate progress curves
    progress_data = []
    for agent in agents:
        progress = []
        start_year = 2025
        end_year = agent.integration_year
        
        for year in years:
            if year < start_year:
                progress.append(0)
            elif year > end_year:
                progress.append(100)
            else:
                # Create S-curve for progress
                x = (year - start_year) / (end_year - start_year)
                progress.append(100 / (1 + np.exp(-10 * (x - 0.5))))
        
        progress_data.append(progress)
    
    fig = go.Figure()
    
    for i, domain in enumerate(domains):
        fig.add_trace(go.Scatter(
            x=years,
            y=progress_data[i],
            name=domain,
            mode='lines',
            line=dict(width=2),
            hovertemplate='Year: %{x:.2f}<br>Progress: %{y:.1f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title='Projected Integration Progress by Domain',
        xaxis_title='Year',
        yaxis_title='Integration Progress (%)',
        height=400,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            range=[0, 100]
        ),
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
            tickmode='array',
            ticktext=[str(year) for year in range(2025, 2036)],
            tickvals=list(range(2025, 2036))
        ),
        hovermode='x unified'
    )
    
    # Add vertical line for current date
    fig.add_vline(
        x=2025,
        line_dash="dash",
        line_color="yellow",
        annotation_text="Present (2025)",
        annotation_position="top",
        annotation_font_size=12,
        annotation_font_color="yellow"
    )
    
    return fig

def main():
    st.title("AI Integration in America Analysis Dashboard")
    
    # Add description
    st.markdown("""
    ### About This Dashboard
    This dashboard presents two distinct approaches to AI integration in America:
    1. **AI Agents' Independent Analysis**: Our specialized AI agents provide their expert analysis and timeline predictions 
    for AI integration across different sectors, based on comprehensive analysis of technological, social, and policy factors.
    2. **OpenAI-US Government Blueprint**: The official roadmap from the OpenAI-US Government partnership, launched in January 2025.
    
    Compare these approaches to understand different perspectives on America's AI integration journey.
    """)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["AI Agents' Timeline", "OpenAI-US Gov Blueprint", "Approach Comparison"])
    
    with tab1:
        st.header("AI Agents' Integration Timeline")
        st.markdown("""
        This timeline shows when each sector is expected to achieve complete AI integration, according to our 
        specialized AI agents' independent analysis. Each agent focuses on a specific domain and provides expert 
        predictions based on current trends, technological capabilities, and societal factors.
        
        **How to Read the Timeline:**
        - Each bar represents an AI agent's domain
        - The length shows the integration journey from 2025 to predicted completion
        - Colors indicate different sectors of society and economy
        - The dashed yellow line marks the present year (2025)
        """)
        
        # Get agents data
        agents = get_all_agents()
        
        # Main timeline
        timeline_fig = create_timeline(agents)
        st.plotly_chart(timeline_fig, use_container_width=True, theme="streamlit")
        
        # Create two columns for additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Integration progress chart
            progress_fig = create_integration_progress_chart(agents)
            st.plotly_chart(progress_fig, use_container_width=True, theme="streamlit")
            
            # Milestone heatmap
            heatmap_fig = create_milestone_heatmap(agents)
            st.plotly_chart(heatmap_fig, use_container_width=True, theme="streamlit")
        
        with col2:
            # Domain relationships network
            network_fig = create_domain_relationships(agents)
            st.plotly_chart(network_fig, use_container_width=True, theme="streamlit")
            
            # Add chart descriptions
            st.markdown("""
            ### Understanding the Visualizations
            
            **Integration Progress Chart**
            Shows the projected progress of AI integration for each domain over time, 
            following an S-curve pattern typical of technology adoption.
            
            **Milestone Density Heatmap**
            Displays the concentration of milestones across different domains and years, 
            helping identify periods of intense development.
            
            **Domain Relationships Network**
            Illustrates the interconnections between different domains based on the timing 
            of their milestones, showing how progress in one area may influence others.
            """)
        
        # Agent details section
        st.header("Detailed Agent Predictions")
        st.markdown("""
        Below are detailed predictions and analysis from each AI agent, providing specialized insights 
        based on their domain expertise.
        """)
        display_agent_details(agents)

    with tab2:
        st.header("OpenAI-US Government Blueprint Timeline")
        st.markdown("""
        This is the official implementation roadmap developed by the OpenAI-US Government partnership. 
        It represents a structured, policy-driven approach to AI integration with defined phases and milestones.
        """)
        
        # Display the blueprint timeline
        blueprint_timeline = create_blueprint_timeline()
        st.plotly_chart(blueprint_timeline, use_container_width=True, theme="streamlit")
        
        # Display detailed timeline in an expander
        with st.expander("View Detailed Timeline"):
            st.markdown("""
            ### Phase 1: Foundation Building (2025-2027)
            - **2025 Q1:** OpenAI-US Government Partnership Kickoff (January 30)
            - **2025 Q2:** Launch of National AI Research Centers
            - **2025 Q3:** Implementation of AI Safety Guidelines
            - **2025 Q4:** Establishment of AI Economic Zones in pilot cities
            - **2026 Q1:** Roll-out of AI Education Initiative
            - **2026 Q2:** Launch of Public-Private AI Infrastructure Partnership
            - **2026 Q4:** First Wave of AI Industry Standards
            - **2027 Q2:** Completion of Initial AI Safety Framework
            
            ### Phase 2: Acceleration (2027-2029)
            - **2027 Q3:** Launch of AI Workforce Transition Program
            - **2027 Q4:** Implementation of Cross-Border AI Collaboration
            - **2028 Q1:** Deployment of AI-Enhanced Public Services
            - **2028 Q3:** Establishment of AI Innovation Hubs
            - **2028 Q4:** Roll-out of National AI Infrastructure
            - **2029 Q2:** Integration of AI in Critical Industries
            
            ### Phase 3: Maturation (2029-2035)
            - **2029 Q3:** Achievement of AI Education Milestones
            - **2029 Q4:** Full Implementation of AI Safety Standards
            - **2030 Q1:** Completion of AI Economic Zone Network
            - **2030 Q3:** Establishment of Global AI Partnership
            - **2030 Q4:** Launch of Advanced AI Research Initiatives
            - **2031 Q2:** Achievement of Full AI Integration Goals
            - **2032 Q1:** Global AI Governance Framework
            - **2032 Q4:** Advanced AI-Human Collaboration Systems
            - **2033 Q2:** Universal AI Education Achievement
            - **2034 Q1:** Quantum-AI Integration Milestone
            - **2034 Q4:** Sustainable AI Infrastructure Complete
            - **2035 Q2:** Full Societal AI Integration Achieved
            """)
    
    with tab3:
        st.header("Approach Comparison Analysis")
        st.markdown("""
        ### Key Differences in Approaches
        
        #### Timeline and Pacing
        - **AI Agents**: Focus on sector-specific integration with varying timelines based on domain complexity
        - **OpenAI-Gov**: Structured three-phase approach with synchronized milestones across sectors
        
        #### Integration Strategy
        - **AI Agents**: Bottom-up approach focusing on technological readiness and sector-specific needs
        - **OpenAI-Gov**: Top-down approach emphasizing policy framework and coordinated implementation
        
        #### Priority Areas
        - **AI Agents**: Emphasizes practical implementation and domain expertise
        - **OpenAI-Gov**: Prioritizes infrastructure, governance, and standardization
        
        #### Risk Management
        - **AI Agents**: Domain-specific risk assessment and mitigation
        - **OpenAI-Gov**: Comprehensive safety framework and phased deployment
        
        ### Areas of Agreement
        - Both approaches recognize the need for:
          - Strong safety guidelines and ethical considerations
          - Public-private partnerships
          - Education and workforce development
          - Global collaboration
        
        ### Notable Insights
        - The AI Agents' approach provides more granular, sector-specific insights
        - The OpenAI-Gov blueprint offers a more coordinated, policy-driven framework
        - Both timelines converge on full integration around 2035
        """)
        
        # Add downloadable report option
        st.download_button(
            label="📥 Download Full Comparison Report",
            data=generate_comparison_report(),
            file_name="ai_integration_approaches_comparison.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
