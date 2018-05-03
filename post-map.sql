ALTER TABLE x_world ADD CreatedTime datetime NOT NULL DEFAULT NOW();

INSERT into total_table SELECT * FROM x_world;
