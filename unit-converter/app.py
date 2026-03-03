from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def perform_conversion(category, value, from_u, to_u):
    if category == "length":
        to_meters = {"millimeter": 0.001, "centimeter": 0.01, "meter": 1, "kilometer": 1000, "inch": 0.0254, "foot": 0.3048, "yard": 0.9144, "mile": 1609.34}
        return (value * to_meters[from_u]) / to_meters[to_u]
    if category == "weight":
        to_grams = {"milligram": 0.001, "gram": 1, "kilogram": 1000, "ounce": 28.3495, "pound": 453.592}
        return (value * to_grams[from_u]) / to_grams[to_u]
    if category == "temperature":
        if from_u == to_u: return value
        c = (value - 32) * 5/9 if from_u == "Fahrenheit" else (value - 273.15 if from_u == "Kelvin" else value)
        if to_u == "Fahrenheit": return (c * 9/5) + 32
        if to_u == "Kelvin": return c + 273.15
        return c
    return 0

@app.route('/')
def home():
    return redirect(url_for('converter', category='length'))

@app.route('/<category>', methods=['GET', 'POST'])
def converter(category):
    # Safety check for valid categories
    valid_categories = ['length', 'weight', 'temperature']
    if category not in valid_categories:
        return redirect(url_for('converter', category='length'))
    
    units = {
        "length": ["millimeter", "centimeter", "meter", "kilometer", "inch", "foot", "yard", "mile"],
        "weight": ["milligram", "gram", "kilogram", "ounce", "pound"],
        "temperature": ["Celsius", "Fahrenheit", "Kelvin"]
    }
    
    result = None
    original_value = None
    from_display = ""
    to_display = ""

    if request.method == 'POST':
        original_value = request.form.get('value')
        from_u = request.form.get('from_unit')
        to_u = request.form.get('to_unit')
        
        if original_value:
            result = perform_conversion(category, float(original_value), from_u, to_u)
            # Log to terminal so you can see it working
            print(f"DEBUG: Converted {original_value} {from_u} to {result} {to_u}")
        
        labels = {"foot": "ft", "centimeter": "cm", "meter": "m", "inch": "in", "Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}
        from_display = labels.get(from_u, from_u)
        to_display = labels.get(to_u, to_u)

    return render_template('converter.html', 
                           category=category, 
                           units=units[category], 
                           result=result, 
                           original_value=original_value, 
                           from_display=from_display, 
                           to_display=to_display)

if __name__ == '__main__':
    app.run(debug=True)