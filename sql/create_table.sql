CREATE TABLE voyages (
    id INT PRIMARY KEY,
    event VARCHAR(50),
    dateStamp INT,
    timeStamp FLOAT,
    voyage_From VARCHAR(50),
    lat DECIMAL(9,6),
    lon DECIMAL(9,6),
    imo_num VARCHAR(20),
    voyage_Id VARCHAR(20),
    allocatedVoyageId VARCHAR(20)
);
