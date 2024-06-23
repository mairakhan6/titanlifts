CREATE TABLE athlete_details (
    athleteID int,
    gender varchar,
    first_name varchar,
    last_name varchar,
    bodyweight float,
    city varchar, 
    contact_number int,
    email varchar,
    PRIMARY KEY (athleteID)
);

CREATE TABLE judge_details (
    judgeID int,
    first_name varchar,
    last_name varchar,
    city varchar,
    PRIMARY KEY (judgeID)
);


CREATE TABLE event_schedule (
    event_id varchar,
    athleteID varchar,
    venue_id varchar,
    event_date date,
    judge1_id varchar,
    judge2_id varchar,
    judge3_id varchar,
    PRIMARY KEY (event_id),
    FOREIGN KEY(judge1_id) REFERENCES judge_details(judge_id),
    FOREIGN KEY(judge2_id) REFERENCES judge_details(judge_id),
    FOREIGN KEY(judge3_id) REFERENCES judge_details(judge_id),
    FOREIGN KEY(athleteID) REFERENCES athlete_details(athleteID),
    FOREIGN KEY(venue_id) REFERENCES venue_details(venue_id)
);

CREATE TABLE venue_details (
    venue_id varchar,
    venue_name varchar,
    city varchar,
    capacity int,
    PRIMARY KEY (venue_id,city)
);

CREATE TABLE event_details (
    event_id INT,
    athleteID INT,
    weight_category INT,
    PRIMARY KEY (event_id),
    FOREIGN KEY (event_id) REFERENCES Event_schedule(event_id),
    FOREIGN KEY(athleteID) REFERENCES athlete_details(athleteID)
);

CREATE TABLE LIFTS (
    athleteID INT,
    lift_num INT,
    lift_type varchar,
    lift_amount VARCHAR,
    PRIMARY KEY (athleteID),
    FOREIGN KEY (athleteID) REFERENCES athlete_details(athleteID) 
);

CREATE TABLE awards (
    athleteID varchar,
    gender varchar,
    weight_lifted float,
    weightclass_position int,
    PRIMARY KEY (athleteID),
    FOREIGN KEY (athleteID) REFERENCES athlete_details(athleteID)
);