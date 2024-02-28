CREATE VIEW View_Events AS
SELECT EVENTS.Title, EVENTS.Description, EVENTS.Date_, EVENTS.Time_, EVENTS.created_timestamp, EVENTS.updated_timestamp, Venues.venue_name
FROM Events
INNER JOIN Venues ON Events.venue_id = Venues.venue_id