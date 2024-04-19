CREATE OR REPLACE FUNCTION func_update_total_after_t1_update()
RETURNS TRIGGER AS
$$
BEGIN
    -- Calculate the sum of marks for the updated record
    DECLARE
        total_t1 INT;
        total_marks_sum INT;
    BEGIN
        total_t1 := NEW.ps + NEW.de + NEW.fcsp_1 + NEW.fsd_1 + NEW.etc + NEW.ci;

        -- Update the t1 column in total_marks for the corresponding enrollment_no
        UPDATE total_marks SET t1 = total_t1 WHERE enrollment_no = NEW.enrollment_no;

        -- Recalculate the total marks for the enrollment_no
        SELECT INTO total_marks_sum t1 + t2 + t3 + t4 FROM total_marks WHERE enrollment_no = NEW.enrollment_no;
        UPDATE total_marks SET total = total_marks_sum WHERE enrollment_no = NEW.enrollment_no;

    END;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trig_update_total_after_t1_update
AFTER UPDATE ON t1_marks
FOR EACH ROW
EXECUTE FUNCTION func_update_total_after_t1_update();



--------------------------------------------------------------------------------------------------------------------------------------



CREATE OR REPLACE FUNCTION func_update_total_after_t2_update()
RETURNS TRIGGER AS
$$
BEGIN
    -- Calculate the sum of marks for the updated record
    DECLARE
        total_t2 INT;
        total_marks_sum INT;
    BEGIN
        total_t2 := NEW.ps + NEW.de + NEW.fcsp_1 + NEW.fsd_1 + NEW.etc + NEW.ci;

        -- Update the t1 column in total_marks for the corresponding enrollment_no
        UPDATE total_marks SET t2 = total_t2 WHERE enrollment_no = NEW.enrollment_no;

        -- Recalculate the total marks for the enrollment_no
        SELECT INTO total_marks_sum t1 + t2 + t3 + t4 FROM total_marks WHERE enrollment_no = NEW.enrollment_no;
        UPDATE total_marks SET total = total_marks_sum WHERE enrollment_no = NEW.enrollment_no;

    END;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trig_update_total_after_t2_update
AFTER UPDATE ON t2_marks
FOR EACH ROW
EXECUTE FUNCTION func_update_total_after_t2_update();



--------------------------------------------------------------------------------------------------------------------------------------



CREATE OR REPLACE FUNCTION func_update_total_after_t3_update()
RETURNS TRIGGER AS
$$
BEGIN
    -- Calculate the sum of marks for the updated record
    DECLARE
        total_t3 INT;
        total_marks_sum INT;
    BEGIN
        total_t3 := NEW.ps + NEW.de + NEW.fcsp_1 + NEW.fsd_1 + NEW.etc + NEW.ci;

        -- Update the t1 column in total_marks for the corresponding enrollment_no
        UPDATE total_marks SET t3 = total_t3 WHERE enrollment_no = NEW.enrollment_no;

        -- Recalculate the total marks for the enrollment_no
        SELECT INTO total_marks_sum t1 + t2 + t3 + t4 FROM total_marks WHERE enrollment_no = NEW.enrollment_no;
        UPDATE total_marks SET total = total_marks_sum WHERE enrollment_no = NEW.enrollment_no;

    END;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trig_update_total_after_t3_update
AFTER UPDATE ON t3_marks
FOR EACH ROW
EXECUTE FUNCTION func_update_total_after_t3_update();




--------------------------------------------------------------------------------------------------------------------------------------




CREATE OR REPLACE FUNCTION func_update_total_after_t4_update()
RETURNS TRIGGER AS
$$
BEGIN
    -- Calculate the sum of marks for the updated record
    DECLARE
        total_t4 INT;
        total_marks_sum INT;
    BEGIN
        total_t4 := NEW.ps + NEW.de + NEW.fcsp_1 + NEW.fsd_1 + NEW.etc + NEW.ci;

        -- Update the t1 column in total_marks for the corresponding enrollment_no
        UPDATE total_marks SET t4 = total_t4 WHERE enrollment_no = NEW.enrollment_no;

        -- Recalculate the total marks for the enrollment_no
        SELECT INTO total_marks_sum t1 + t2 + t3 + t4 FROM total_marks WHERE enrollment_no = NEW.enrollment_no;
        UPDATE total_marks SET total = total_marks_sum WHERE enrollment_no = NEW.enrollment_no;

    END;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trig_update_total_after_t4_update
AFTER UPDATE ON t4_marks
FOR EACH ROW
EXECUTE FUNCTION func_update_total_after_t4_update();




--------------------------------------------------------------------------------------------------------------------------------------




CREATE OR REPLACE FUNCTION func_update_student_ranks()
RETURNS TRIGGER AS $$
BEGIN
    -- Step 1: Calculate and Update Ranks in total_marks
    WITH ranked_totals AS (
        SELECT
            enrollment_no,
            RANK() OVER (ORDER BY total DESC) AS calculated_rank
        FROM
            total_marks
    )
    UPDATE total_marks tm
    SET
        rank = rt.calculated_rank
    FROM
        ranked_totals rt
    WHERE
        tm.enrollment_no = rt.enrollment_no;
    
    -- Step 2: Sync Ranks to student_details
    UPDATE student_details sd
    SET
        rank = tm.rank
    FROM
        total_marks tm
    WHERE
        sd.enrollment_no = tm.enrollment_no;

    -- Since it's an AFTER trigger, RETURN NULL is used
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_update_student_ranks
AFTER INSERT OR UPDATE OF total ON total_marks
FOR EACH ROW
EXECUTE FUNCTION func_update_student_ranks();

