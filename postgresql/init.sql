CREATE TYPE suburb_type as ENUM ('Aeropuerto','Barrio','Colonia','Condominio',
								   'Ejido','Equipamiento','Fraccionamiento','Granja','Hacienda','Paraje','Parque industrial',
								   'Pueblo','Ranchería','Rancho','Unidad habitacional','Zona comercial','Zona federal','Zona industrial',
								  'Zona militar');
CREATE TYPE zone as ENUM ('Urbano','Rural','Semiurbano');

CREATE TABLE state(
	"id" BIGSERIAL UNIQUE NOT NULL,
	"code" VARCHAR(10) UNIQUE NOT NULL,
	"name" VARCHAR(100) UNIQUE NOT NULL,
	PRIMARY KEY(id)
);

CREATE INDEX ON "state"("id");
CREATE INDEX ON "state"("code");
CREATE INDEX ON "state"("name");

CREATE TABLE town(
	"id" BIGSERIAL UNIQUE NOT NULL,
	"town_id" VARCHAR(5) NOT NULL,
	"town_name" VARCHAR(100) NOT NULL,
	"city_id" VARCHAR(5) NULL,
	"city_name" VARCHAR(100) NULL,
	"state_id" BIGINT NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT fk_state
	FOREIGN KEY(state_id)
		REFERENCES state(id)
		ON DELETE CASCADE
);

CREATE INDEX ON "town"("id");
CREATE INDEX ON "town"("town_name");
CREATE INDEX ON "town"("city_name");

CREATE TABLE suburb(
	"id" BIGSERIAL UNIQUE NOT NULL,
	"unique_suburb_town_id" VARCHAR(100) NOT NULL,
	"name" VARCHAR(50) NOT NULL,
	"postal_code" INT NOT NULL,
	"postal_code_administration" INT NOT NULL,
	"postal_code_office" INT NOT NULL,
	"cp" VARCHAR(10) NULL,
	"code_type" VARCHAR(5) NOT NULL,
	"type" suburb_type NOT NULL,
	"zone" zone NOT NULL,
	"town_id" BIGINT NOT NULL,
	PRIMARY KEY(id,unique_suburb_town_id),
	CONSTRAINT fk_town
	FOREIGN KEY(town_id)
		REFERENCES town(id)
		ON DELETE CASCADE
);

CREATE INDEX ON "suburb"("name");
CREATE INDEX ON "suburb"("id");
CREATE INDEX ON "suburb"("unique_suburb_town_id");
CREATE INDEX ON "suburb"("postal_code");


CREATE TABLE "user"(
	"id" BIGSERIAL UNIQUE NOT NULL,
	"name" VARCHAR(100) NOT NULL,
	"last_name" VARCHAR(100) NOT NULL,
	"username" VARCHAR(150) UNIQUE NOT NULL,
	"password" BYTEA NOT NULL,
	PRIMARY KEY(id,username)
);

CREATE INDEX ON "user"("id");
CREATE INDEX ON "user"("username");


/*CRUD FUNCTIONS------------------------------------------------*/


/*CRUD STATE------------------------------------------------*/
/*INSERT-------------------------------------------------*/
CREATE OR REPLACE FUNCTION insert_state(_code VARCHAR(10),_name VARCHAR(100))
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM state WHERE UPPER(name) = UPPER(_name) OR code = _code) THEN
			message := 'This state already exists.';
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		INSERT INTO state("code","name") VALUES(_code,_name) RETURNING id INTO _id;
		success := true;
		message := 'OK';
		status_code := 201;
		data := JSON_BUILD_OBJECT('id',_id,'code',_code,'name',_name);
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

/*READ-------------------------------------------------*/
CREATE OR REPLACE FUNCTION read_state(VARCHAR(100)[],int,int)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	BEGIN
		RETURN JSON_BUILD_OBJECT('success',true,'message','OK','statusCode',200,'data',
						(SELECT ARRAY_TO_JSON(ARRAY_AGG(dt))
	FROM (SELECT *
		 FROM state 
		 WHERE ( $1 IS NULL OR name = ANY  ($1))
		 ORDER BY id DESC
		 LIMIT $2 OFFSET $3) AS dt));
	END;
$$;

/*UPDATE-------------------------------------------------*/
CREATE OR REPLACE FUNCTION update_state(_id INT,_code VARCHAR(10),_name VARCHAR(100))
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		current_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM state where id = _id) THEN
			IF NOT EXISTS(SELECT * FROM state where NOT id = _id AND (UPPER(name) = UPPER(_name) OR code = _code)) THEN
				UPDATE state set name = _name, code = _code WHERE id = _id RETURNING id INTO current_id;
				success := true;
				message := 'OK';
				status_code := 200;
				data := JSON_BUILD_OBJECT('id',current_id,'code',_code,'name',_name);
				RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
			END IF;
			message := 'This state already exists.';
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		status_code := 404;
		message := 'That state does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;


/*DELETE-------------------------------------------------*/
CREATE OR REPLACE FUNCTION delete_state(_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
	BEGIN
		IF EXISTS(SELECT * FROM state where id = _id) THEN
			DELETE FROM state where id = _id;
			success := true;
			message := 'OK';
			status_code := 200;
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',NULL);
		END IF;
		status_code := 404;
		message := 'That state does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;


/*CRUD TOWN------------------------------------------------*/
/*INSERT-------------------------------------------------*/
CREATE OR REPLACE FUNCTION insert_town(_town_id VARCHAR(5),_town_name VARCHAR(100),
									   _city_id VARCHAR(5),_city_name VARCHAR(100),_state_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM state where id = _state_id) THEN
			IF EXISTS(SELECT * FROM town WHERE state_id = _state_id AND (town_id = _town_id OR UPPER(town_name) = UPPER(_town_name))) THEN
				message := 'Verify that the state is registered and that the town does not repeat itself';
				RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
			END IF;
			INSERT INTO town("town_id","town_name","city_id","city_name","state_id") 
				VALUES(_town_id,_town_name,_city_id,_city_name,_state_id) RETURNING id INTO _id;
			success := true;
			message := 'OK';
			status_code := 201;
			data := JSON_BUILD_OBJECT('id',_id,'townId',_town_id,'townName',_town_name,'cityId',_city_id,'cityName',_city_name,'stateId',_state_id);
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		status_code := 404;
		message := 'That state does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

/*READ-------------------------------------------------*/
CREATE OR REPLACE FUNCTION read_town(VARCHAR(100)[],VARCHAR(100)[],int,int)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	BEGIN
		RETURN JSON_BUILD_OBJECT('success',true,'message','OK','statusCode',200,'data',
						(SELECT ARRAY_TO_JSON(ARRAY_AGG(dt))
	FROM (SELECT *
		 FROM town 
		 WHERE ( $1 IS NULL OR town_name = ANY  ($1))
		 AND ( $2 IS NULL OR city_name = ANY  ($2))
		 ORDER BY id DESC
		 LIMIT $3 OFFSET $4) AS dt));
	END;
$$;

/*UPDATE-------------------------------------------------*/
CREATE OR REPLACE FUNCTION update_town(_id INT,_town_id VARCHAR(5),_town_name VARCHAR(100),
									   _city_id VARCHAR(5),_city_name VARCHAR(100),_state_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		current_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM town where id = _id) THEN
			IF EXISTS(SELECT * FROM state where id = _state_id) THEN
				IF NOT EXISTS(SELECT * FROM town WHERE NOT id = _id AND state_id = _state_id AND 
							  (town_id = _town_id OR UPPER(town_name) = UPPER(_town_name))) THEN
					UPDATE town set town_id = _town_id, town_name = _town_name, city_id = _city_id,
						city_name = _city_name, state_id = _state_id WHERE id = _id RETURNING id INTO current_id;
					success := true;
					message := 'OK';
					status_code := 200;
					data := JSON_BUILD_OBJECT('id',current_id,'townId',_town_id,'townName',_town_name,'cityId',_city_id,'cityName',_city_name,'stateId',_state_id);
					RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
				END IF;
				message := 'That town already exists';
				RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
			END IF;
			status_code := 404;
			message := 'That state does not exist';
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		status_code := 404;
		message := 'That town does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;


/*DELETE-------------------------------------------------*/
CREATE OR REPLACE FUNCTION delete_town(_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
	BEGIN
		IF EXISTS(SELECT * FROM town where id = _id) THEN
			DELETE FROM town where id = _id;
			success := true;
			message := 'OK';
			status_code := 200;
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',NULL);
		END IF;
		status_code := 404;
		message := 'That town does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

/*CRUD SUBURB------------------------------------------------*/
/*INSERT-------------------------------------------------*/
CREATE OR REPLACE FUNCTION insert_suburb(_unique_suburb_town_id VARCHAR(100),_name VARCHAR(50),
									   _postal_code INT,_postal_code_administration INT,_postal_code_office INT,
										_cp VARCHAR(10),_code_type VARCHAR(5),_type suburb_type,_zone zone,_town_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM town where id = _town_id) THEN
			IF EXISTS(SELECT * FROM suburb WHERE town_id = _town_id AND (unique_suburb_town_id = _unique_suburb_town_id OR UPPER(name) = UPPER(_name))) THEN
				message := 'Verify that the town is registered and that the suburb does not repeat itself';
				RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
			END IF;
			INSERT INTO suburb("unique_suburb_town_id","name","postal_code","postal_code_administration",
							 "postal_code_office","cp","code_type","type","zone","town_id") 
				VALUES(_unique_suburb_town_id,_name,_postal_code,_postal_code_administration,
					   _postal_code_office,_cp,_code_type,_type,_zone,_town_id) RETURNING id INTO _id;
			success := true;
			message := 'OK';
			status_code := 201;
			data := JSON_BUILD_OBJECT('id',_id,'uniqueSuburbTownId',_unique_suburb_town_id,'name',_name,'postalCode',
									  _postal_code,'postalCodeAdministration',_postal_code_administration,'postalCodeOffice',_postal_code_office,
									 'cp',_cp,'codeType',_code_type,'type',_type,'zone',_zone,'townId',_town_id);
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		status_code := 404;
		message := 'That town does not exist.';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

/*READ-------------------------------------------------*/
CREATE OR REPLACE FUNCTION read_suburb(INT[],VARCHAR(50)[],int,int)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	BEGIN
		RETURN JSON_BUILD_OBJECT('success',true,'message','OK','statusCode',200,'data',
						(SELECT ARRAY_TO_JSON(ARRAY_AGG(dt))
	FROM (SELECT *
		 FROM suburb 
		 WHERE ( $1 IS NULL OR postal_code = ANY  ($1))
		 AND ( $2 IS NULL OR name = ANY  ($2))
		 ORDER BY id DESC
		 LIMIT $3 OFFSET $4) AS dt));
	END;
$$;

/*UPDATE-------------------------------------------------*/
CREATE OR REPLACE FUNCTION update_suburb(_id INT,_unique_suburb_town_id VARCHAR(100),_name VARCHAR(50),
									   _postal_code INT,_postal_code_administration INT,_postal_code_office INT,
										_cp VARCHAR(10),_code_type VARCHAR(5),_type suburb_type,_zone zone,_town_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		current_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM suburb where id = _id) THEN
			IF EXISTS(SELECT * FROM town where id = _town_id) THEN
				IF NOT EXISTS(SELECT * FROM suburb WHERE NOT id = _id AND town_id = _town_id AND 
							  (unique_suburb_town_id = _unique_suburb_town_id OR UPPER(name) = UPPER(_name))) THEN
					UPDATE suburb set unique_suburb_town_id = _unique_suburb_town_id, name = _name, postal_code = _postal_code,
						postal_code_administration = _postal_code_administration, postal_code_office = _postal_code_office,
						cp = _cp, code_type = _code_type, type = _type, zone = _zone, town_id = _town_id WHERE id = _id RETURNING id INTO current_id;
					success := true;
					message := 'OK';
					status_code := 200;
					data := JSON_BUILD_OBJECT('id',current_id,'uniqueSuburbTownId',_unique_suburb_town_id,'name',_name,'postalCode',
									  _postal_code,'postalCodeAdministration',_postal_code_administration,'postalCodeOffice',_postal_code_office,
									 'cp',_cp,'codeType',_code_type,'type',_type,'zone',_zone,'townId',_town_id);
					RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
				END IF;
				message := 'That suburb already exists';
				RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
			END IF;
			status_code := 404;
			message := 'That town does not exist';
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		status_code := 404;
		message := 'That suburb does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

/*DELETE-------------------------------------------------*/
CREATE OR REPLACE FUNCTION delete_suburb(_id INT)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 404;
		success BOOLEAN DEFAULT false;
	BEGIN
		IF EXISTS(SELECT * FROM suburb where id = _id) THEN
			DELETE FROM suburb where id = _id;
			success := true;
			message := 'OK';
			status_code := 200;
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',NULL);
		END IF;
		message := 'That suburb does not exist';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

/*REGISTER FUNCTIONS------------------------------------------------*/
/*REGISTER USER-------------------------------------------------*/

CREATE OR REPLACE FUNCTION insert_user(_name VARCHAR(100),_last_name VARCHAR(100),_username VARCHAR(150), _password BYTEA)
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 400;
		success BOOLEAN DEFAULT false;
		_id INT;
	BEGIN
		IF EXISTS(SELECT * FROM "user" WHERE UPPER(username) = UPPER(_username)) THEN
			message := 'This username already exists.';
			RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
		END IF;
		INSERT INTO "user"("name","last_name","username","password") VALUES(_name,_last_name,_username,_password) RETURNING id INTO _id;
		success := true;
		message := 'OK';
		status_code := 201;
		data := JSON_BUILD_OBJECT('id',_id,'_name',_name,'lastName',_last_name,'username',_username);
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;


/*REGISTER USER-------------------------------------------------*/
CREATE OR REPLACE FUNCTION read_user(_username VARCHAR(150))
	RETURNS JSON
	LANGUAGE 'plpgsql' AS $$
	DECLARE
		message VARCHAR;
		data JSON DEFAULT NULL;
		status_code INT DEFAULT 404;
		success BOOLEAN DEFAULT false;
	BEGIN
		IF EXISTS(SELECT * FROM "user" WHERE UPPER(username) = UPPER(_username)) THEN
			data := ROW_TO_JSON(t) from (select id,name,last_name,username,encode(password, 'base64') as password
										 from "user" WHERE UPPER(username) = UPPER(_username)) t;
			RETURN JSON_BUILD_OBJECT('success',true,'message','OK','statusCode',200,'data',data);
		END IF;
		message := 'This username does not exist.';
		RETURN JSON_BUILD_OBJECT('success',success,'message',message,'statusCode',status_code,'data',data);
	END;
$$;

--TESTS-------------------------------------------------------------------------
------STATE---------------------
--SELECT * FROM insert_state('001','Coahuila');
--SELECT * FROM read_state(ARRAY['Chiapas'],10,0);
--SELECT * FROM read_state(null,10,0);
--SELECT * FROM update_state(3,'001','Chiapas');
--SELECT * FROM delete_state(1);

------TOWN---------------------
--SELECT * FROM insert_town('03','La paz',null,null,4);
--SELECT * FROM read_town(null,ARRAY['city'],10,0);
--SELECT * FROM read_town(ARRAY['town'],null,10,0);
--SELECT * FROM read_town(null,null,10,0);
--SELECT * FROM update_town(8,'03','mexicali',null,null,4);
--SELECT * FROM delete_town(9);

------SUBURB---------------------
--SELECT * FROM insert_suburb('06','Palmas',35158,35158,35158,NULL,'48','Pueblo','Rural',8);
--SELECT * FROM read_suburb(ARRAY[35158],null,10,0);
--SELECT * FROM read_suburb(null,ARRAY['Palmas'],10,0);
--SELECT * FROM read_suburb(null,null,10,0);
--SELECT * FROM update_suburb(2,'01','Miguel Aleman',36543,36543,36543,null,'01','Granja','Urbano',8);
--SELECT * FROM delete_suburb(3);

------USER-------------------------
--SELECT * FROM insert_user('javier','navarrete','javiernafa',bytea);
--SELECT * FROM read_user('javiernava');

