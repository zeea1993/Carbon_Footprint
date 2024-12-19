import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to calculate the carbon footprints
def calculate_energy_footprint(electricity_bill, gas_bill, fuel_bill):
    return (
        electricity_bill * 12 * 0.0005 +
        gas_bill * 12 * 0.0053 +
        fuel_bill * 12 * 2.32
    )

def calculate_waste_footprint(total_waste, recycling_percentage):
    return total_waste * 12 * (0.57 - recycling_percentage)

def calculate_travel_footprint(km_traveled, fuel_efficiency):
    return km_traveled * (1 / fuel_efficiency) * 2.31

def generate_suggestions(energy_footprint, waste_footprint, travel_footprint):
    suggestions = []
    if energy_footprint > 1000:
        suggestions.append("Consider switching to renewable energy sources or energy-efficient appliances.")
    if waste_footprint > 500:
        suggestions.append("Increase recycling or composting efforts to reduce waste emissions.")
    if travel_footprint > 1000:
        suggestions.append("Encourage remote meetings and consider hybrid or electric vehicles.")
    return suggestions

# Function to generate the PDF content
def generate_pdf(energy_footprint, waste_footprint, travel_footprint, total_footprint, suggestions):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Add some content to the PDF
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Carbon Footprint Report")
    c.drawString(50, 730, f"Energy Footprint: {energy_footprint:.2f} kgCO2")
    c.drawString(50, 710, f"Waste Footprint: {waste_footprint:.2f} kgCO2")
    c.drawString(50, 690, f"Business Travel Footprint: {travel_footprint:.2f} kgCO2")
    c.drawString(50, 670, f"Total Carbon Footprint: {total_footprint:.2f} kgCO2")

    c.drawString(50, 650, f"Suggestions for Reducing Your Carbon Footprint:")
    y_position = 630
    for suggestion in suggestions:
        c.drawString(50, y_position, f"- {suggestion}")
        y_position -= 20

    # Save the PDF to the buffer
    c.showPage()
    c.save()
    
    # Get the PDF content as bytes
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content

# Function to generate a bar chart
def generate_bar_chart(energy_footprint, waste_footprint, travel_footprint, total_footprint):
    categories = ['Energy', 'Waste', 'Travel', 'Total']
    values = [energy_footprint, waste_footprint, travel_footprint, total_footprint]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categories, values, color=['blue', 'green', 'orange', 'red'])
    ax.set_ylabel('Carbon Footprint (kgCO2)')
    ax.set_title('Carbon Footprint Breakdown')

    # Save the chart to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)
    return chart_buffer

# Streamlit app
st.title("Carbon Footprint Monitoring Tool")

# Input fields for energy usage
st.header("Energy Usage")
electricity_bill = st.number_input("Enter your average monthly electricity bill (in euros):", min_value=0.0, step=1.0)
gas_bill = st.number_input("Enter your average monthly natural gas bill (in euros):", min_value=0.0, step=1.0)
fuel_bill = st.number_input("Enter your average monthly fuel bill for transportation (in euros):", min_value=0.0, step=1.0)

# Input fields for waste management
st.header("Waste Management")
total_waste = st.number_input("Enter the total waste you generate per month (in kg):", min_value=0.0, step=1.0)
recycling_percentage = st.slider("Enter the percentage of waste recycled or composted:", min_value=0, max_value=100, step=1) / 100

# Input fields for business travel
st.header("Business Travel")
km_traveled = st.number_input("Enter the total kilometers traveled per year for business purposes:", min_value=0.0, step=1.0)
fuel_efficiency = st.number_input("Enter the average fuel efficiency of vehicles (in liters per 100 km):", min_value=0.1, step=0.1)

# Calculate carbon footprint when button is pressed
if st.button("Calculate Carbon Footprint"):
    # Calculate the carbon footprints
    energy_footprint = calculate_energy_footprint(electricity_bill, gas_bill, fuel_bill)
    waste_footprint = calculate_waste_footprint(total_waste, recycling_percentage)
    travel_footprint = calculate_travel_footprint(km_traveled, fuel_efficiency)

    total_footprint = energy_footprint + waste_footprint + travel_footprint

    # Generate suggestions for reducing footprint
    suggestions = generate_suggestions(energy_footprint, waste_footprint, travel_footprint)

    # Display the carbon footprint results
    st.subheader("Carbon Footprint Report")
    st.write(f"**Energy Footprint:** {energy_footprint:.2f} kgCO2")
    st.write(f"**Waste Footprint:** {waste_footprint:.2f} kgCO2")
    st.write(f"**Business Travel Footprint:** {travel_footprint:.2f} kgCO2")
    st.write(f"**Total Carbon Footprint:** {total_footprint:.2f} kgCO2")

    st.subheader("Suggestions for Reducing Your Carbon Footprint")
    if suggestions:
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
    else:
        st.write("Great job! Your carbon footprint is within reasonable limits.")

    # Generate and display the bar chart
    chart_buffer = generate_bar_chart(energy_footprint, waste_footprint, travel_footprint, total_footprint)
    st.image(chart_buffer, caption="Carbon Footprint Breakdown", use_column_width=True)

    # Generate the PDF content and provide download link
    pdf_content = generate_pdf(energy_footprint, waste_footprint, travel_footprint, total_footprint, suggestions)
    st.download_button(
        label="Download PDF Report",
        data=pdf_content,
        file_name="carbon_footprint_report.pdf",
        mime="application/pdf"
    )
