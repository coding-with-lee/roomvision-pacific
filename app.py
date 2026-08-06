from flask import Flask, render_template, request, jsonify
import urllib.parse

app = Flask(__name__)

BASE_PRICES = {
    "mahogany_bed": 35000,
    "l_sofa": 45000,
    "dining_table": 40000
}

FINISH_MULTIPLIERS = {
    "clear_varnish": 1.0,
    "dark_mahogany": 1.1,
    "matt_black": 1.15
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calculate-quote", methods=["POST"])
def calculate_quote():
    data = request.json
    
    product_type = data.get("product_type", "mahogany_bed")
    length_ft = float(data.get("length_ft", 6))
    width_ft = float(data.get("width_ft", 6))
    finish = data.get("finish", "clear_varnish")
    customer_phone = data.get("phone", "")
    customer_name = data.get("name", "")

    base_price = BASE_PRICES.get(product_type, 35000)
    area_sq_ft = length_ft * width_ft
    size_factor = area_sq_ft / 36.0  
    finish_multiplier = FINISH_MULTIPLIERS.get(finish, 1.0)
    
    total_quote = round(base_price * size_factor * finish_multiplier)
    
    sales_phone = "254700000000"
    
    message = (
        f"🛋️ *New RoomVision Lead - Modern Pacific*\n\n"
        f"👤 *Customer:* {customer_name}\n"
        f"📞 *Phone:* {customer_phone}\n"
        f"📦 *Item:* {product_type.replace('_', ' ').title()}\n"
        f"📐 *Space Dimensions:* {length_ft}ft x {width_ft}ft\n"
        f"🎨 *Finish:* {finish.replace('_', ' ').title()}\n"
        f"💰 *Estimated Quote:* KES {total_quote:,}\n\n"
        f"_Sent via RoomVision Web App_"
    )
    
    whatsapp_url = f"https://wa.me/{sales_phone}?text={urllib.parse.quote(message)}"
    
    return jsonify({
        "status": "success",
        "estimated_price": f"KES {total_quote:,}",
        "whatsapp_url": whatsapp_url
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)