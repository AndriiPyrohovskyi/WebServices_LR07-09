from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from src.external_api.service import service
from src.external_api.models import F1DataModel, F1ProcessedModel


router = APIRouter(prefix="/external", tags=["External F1 API"])


@router.get("/data/drivers", response_model=F1DataModel)
def get_raw_drivers_data() -> F1DataModel:
    """
    Get raw driver data from F1 API for the current season.
    Returns unprocessed data directly from Ergast API.
    """
    try:
        return service.get_current_season_drivers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching drivers data: {str(e)}")


@router.get("/data/races", response_model=F1DataModel)
def get_raw_races_data() -> F1DataModel:
    """
    Get raw race calendar data from F1 API for the current season.
    Returns unprocessed data directly from Ergast API.
    """
    try:
        return service.get_current_season_races()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching races data: {str(e)}")


@router.get("/data/standings", response_model=F1DataModel)
def get_raw_standings_data(
    season: Optional[str] = Query(
        "current", description="Season year (e.g., 2024) or 'current'"
    )
) -> F1DataModel:
    """
    Get raw driver standings data from F1 API.
    Returns unprocessed data directly from Ergast API.
    
    - **season**: Specify a year (e.g., 2024) or use 'current' for the latest season
    """
    try:
        return service.get_driver_standings(season)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching standings data: {str(e)}"
        )


@router.get("/processed/drivers", response_model=F1ProcessedModel)
def get_processed_drivers() -> F1ProcessedModel:
    """
    Get processed and formatted driver data for the current F1 season.
    Returns cleaned and structured data with summary information.
    """
    try:
        raw_data = service.get_current_season_drivers()
        return service.process_drivers_data(raw_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing drivers data: {str(e)}"
        )


@router.get("/processed/races", response_model=F1ProcessedModel)
def get_processed_races() -> F1ProcessedModel:
    """
    Get processed and formatted race calendar for the current F1 season.
    Returns cleaned and structured data with race details and locations.
    """
    try:
        raw_data = service.get_current_season_races()
        return service.process_races_data(raw_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing races data: {str(e)}"
        )


@router.get("/processed/standings", response_model=F1ProcessedModel)
def get_processed_standings(
    season: Optional[str] = Query(
        "current", description="Season year (e.g., 2024) or 'current'"
    )
) -> F1ProcessedModel:
    """
    Get processed and formatted driver championship standings.
    Returns cleaned and structured data with driver positions, points, and wins.
    
    - **season**: Specify a year (e.g., 2024) or use 'current' for the latest season
    """
    try:
        raw_data = service.get_driver_standings(season)
        return service.process_standings_data(raw_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing standings data: {str(e)}"
        )


@router.get("/f1/html", response_class=HTMLResponse)
def get_f1_html(
    season: Optional[str] = Query(
        "current", description="Season year (e.g., 2024) or 'current'"
    )
) -> str:
    """
    Return an HTML page displaying F1 championship standings with styled layout.
    Shows driver positions, points, teams, and wins in a formatted table.
    """
    try:
        raw_data = service.get_driver_standings(season)
        processed_data = service.process_standings_data(raw_data)

        # Generate table rows
        table_rows = ""
        for item in processed_data.items:
            position_class = ""
            if item["position"] == 1:
                position_class = "gold"
            elif item["position"] == 2:
                position_class = "silver"
            elif item["position"] == 3:
                position_class = "bronze"

            table_rows += f"""
            <tr class="{position_class}">
                <td>{item['position']}</td>
                <td><strong>{item['driver_name']}</strong></td>
                <td>{item['driver_code']}</td>
                <td>{item['nationality']}</td>
                <td>{item['team']}</td>
                <td>{item['points']}</td>
                <td>{item['wins']}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{processed_data.title}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                }}
                h1 {{
                    color: #e10600;
                    text-align: center;
                    margin-bottom: 10px;
                    font-size: 2.5rem;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }}
                .description {{
                    text-align: center;
                    color: #666;
                    margin-bottom: 20px;
                    font-size: 1.1rem;
                }}
                .summary {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 25px;
                    border-left: 4px solid #e10600;
                    color: #333;
                    font-size: 1rem;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                thead {{
                    background: linear-gradient(135deg, #e10600 0%, #ff1e00 100%);
                    color: white;
                }}
                th {{
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                    text-transform: uppercase;
                    font-size: 0.9rem;
                    letter-spacing: 1px;
                }}
                td {{
                    padding: 12px 15px;
                    border-bottom: 1px solid #eee;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .gold {{
                    background-color: #ffd70033 !important;
                }}
                .silver {{
                    background-color: #c0c0c033 !important;
                }}
                .bronze {{
                    background-color: #cd7f3233 !important;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 0.9rem;
                }}
                .footer a {{
                    color: #e10600;
                    text-decoration: none;
                    font-weight: 600;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏎️ {processed_data.title}</h1>
                <p class="description">{processed_data.description}</p>
                <div class="summary">
                    <strong>📊 Summary:</strong> {processed_data.summary}
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Pos</th>
                            <th>Driver</th>
                            <th>Code</th>
                            <th>Nationality</th>
                            <th>Team</th>
                            <th>Points</th>
                            <th>Wins</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                
                <div class="footer">
                    <p>Data provided by <a href="http://ergast.com/mrd/" target="_blank">Ergast F1 API</a></p>
                    <p>Season: {processed_data.season} | Total Drivers: {processed_data.total_items}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    except Exception as e:
        return f"""
        <html>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h2 style="color: #e10600;">⚠️ Error Loading F1 Data</h2>
                <p style="color: #666;">{str(e)}</p>
            </body>
        </html>
        """
