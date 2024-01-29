from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Read the CSV file into a pandas DataFrame
full_df = pd.read_csv('https://zupload1015.s3.eu-north-1.amazonaws.com/parsed_data.csv')

@app.route('/')
def index():
    global full_df
    def map_position(position):
        if position.startswith('GK'):
            return 1
        elif position.startswith('DM'):
            return 3
        elif position.startswith('WB'):
            return 2.5  # You can use any value between 2 and 3
        elif position.startswith('D'):
            return 2
        elif position.startswith('M'):
            return 4
        elif position.startswith('A'):
            return 5
        elif position.startswith('S'):
            return 6
        else:
            return 7
    # Add a new column 'MappedPosition' based on the mapping function
    full_df['MappedPosition'] = full_df['Position'].apply(map_position)

    # Sort the DataFrame by 'MappedPosition'
    
    # Select specific columns
    selected_columns = ['MappedPosition','Inf', 'Name', 'Age', 'Wage', 'Transfer Value', 'Nationality', 'Position', 'Personality', 'Av Rat', 'Mins', 'Gls', 'Ast', 'NP-xG/90', 'xA/90']
    df = full_df[selected_columns]

    # Replace NaN values in the 'Inf' and personality columns with an empty string
    df['Inf'] = df['Inf'].fillna('')
    df['Personality'] = df['Personality'].fillna('')

    return render_template('index.html', table=df.sort_values(by='MappedPosition'))

@app.route('/player/<name>')
def player_page(name):
    # Filter the DataFrame based on the selected name
    player_df = full_df[full_df['Name'] == name]

    # Check if the player was found
    if player_df.empty:
        return render_template('player_not_found.html', name=name)

    # Convert the player DataFrame to HTML
    player_html = player_df.to_html(classes='table table-dark', index=False)

    return render_template('player.html', name=name, player_df=player_df, player_table=player_html)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=True)
