
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from scraper import get_vinyl_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vinyl_scout_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Search {self.search_query}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Save to history
            history = SearchHistory(search_query=query)
            db.session.add(history)
            db.session.commit()
            
            # Get data
            data = get_vinyl_data(query)
            
            # Check for partial request
            if request.args.get('partial') == 'true' or request.form.get('partial') == 'true':
                return render_template('partials/results_content.html', data=data)
                
            return render_template('results.html', data=data)
    
    recent_searches = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(5).all()
    return render_template('index.html', recent_searches=recent_searches)

@app.route('/api/search')
def api_search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    data = get_vinyl_data(query)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
