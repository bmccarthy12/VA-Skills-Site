import React, { useEffect, useState } from "react";
import "../styles.css"; // Ensure this file is correctly imported

const TeamsTable = () => {
    const [teams, setTeams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Paths to JSON files in public folder
    const SKILLS_JSON_URL = "/skills_list.json";
    const TEAMS_JSON_URL = "/team_list.json";
    const QUALIFIED_JSON_URL = "/qualified.json"; // New file for qualified teams

    useEffect(() => {
        async function fetchTeams() {
            try {
                // Fetch all JSON data concurrently
                const [skillsResponse, teamsResponse, qualifiedResponse] = await Promise.all([
                    fetch(SKILLS_JSON_URL),
                    fetch(TEAMS_JSON_URL),
                    fetch(QUALIFIED_JSON_URL)
                ]);

                if (!skillsResponse.ok || !teamsResponse.ok || !qualifiedResponse.ok) {
                    throw new Error("Failed to fetch data.");
                }

                const skillsData = await skillsResponse.json();
                const teamsData = await teamsResponse.json();
                const qualifiedData = await qualifiedResponse.json();

                // Extract qualified team names into a Set for fast lookup
                const qualifiedTeams = new Set(Object.values(qualifiedData.team_name));

                // Merge team info with skills data
                const mergedData = skillsData.map(skill => {
                    const teamInfo = teamsData.find(team => team.team_id === skill.team_number) || {};
                    const isQualified = qualifiedTeams.has(skill.team_name); // Check qualification

                    return {
                        rank: 0, // Will be set after sorting
                        team_number: teamInfo.team_number,
                        team_name: teamInfo.team_name || "Unknown",
                        programming_score: skill.programming_score,
                        driver_score: skill.driver_score,
                        total_score: skill.total_score,
                        highest_auto: skill.highest_auto,
                        highlight: isQualified ? "green" : "" // Apply green highlight if qualified
                    };
                });

                // Sort teams by total score (highest to lowest)
                mergedData.sort((a, b) => {
                    if (b.total_score === a.total_score) {
                        if (b.highest_auto === a.highest_auto) {
                            return b.driver_score - a.driver_score;
                        }
                        return b.highest_auto - a.highest_auto;
                    }
                    return b.total_score - a.total_score;
                });

                // Assign ranks after sorting
                mergedData.forEach((team, index) => {
                    team.rank = index + 1;
                });

                let totalHighlighted = mergedData.filter(team => team.highlight === "green").length;
                
                // Highlight additional top teams in yellow until we reach 56 total
                for (let i = 0; i < mergedData.length && totalHighlighted < 56; i++) {
                    if (mergedData[i].highlight === "") {
                        mergedData[i].highlight = "yellow";
                        totalHighlighted++;
                    }
                }

                setTeams(mergedData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchTeams();
    }, []);

    if (loading) return <p>Loading teams...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="container">
            <h2 className="title">Virginia VRC Teams - Skills Scores</h2>
            <p className="highlight-info">
                <span className="green-highlight">Green highlight</span>: "Already Qualified" and 
                <span className="yellow-highlight">Yellow highlight</span>: "Will Qualify if Season Ends Today"
            </p>
            <p className="disclaimer">Results are unofficial and no guarantee of accuracy; Tie-Breakers not calculated</p>
            <div className="table-container">
                <table>
                    <colgroup>
                        <col />
                        <col />
                        <col />
                        <col />
                    </colgroup>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Total Score</th>
                            <th>Programming Score</th>
                            <th>Driver Score</th>
                            <th>Team Number</th>
                            <th>Team Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        {teams.map((team) => (
                            <tr key={team.team_number} className={team.highlight}>
                                <td>{team.rank}</td>
                                <td>{team.total_score}</td>
                                <td>{team.programming_score}</td>
                                <td>{team.driver_score}</td>
                                <td>{team.team_number}</td>
                                <td>{team.team_name}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TeamsTable;
