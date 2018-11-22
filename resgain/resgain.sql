create table complete_information(
id int auto_increment primary key,
name varchar(10) not null,
man varchar(10) not null,
girl varchar(10) not null,
details varchar(1000) not null,
five_lines varchar(10) not null,
three_talents varchar(10) not null,
five_cases_tian int not null,
five_cases_ren int not null,
five_cases_di int not null,
five_cases_zong int not null,
five_cases_wai int not null,
five_grid_analysis_tian varchar(255) not null,
five_grid_analysis_ren varchar(255) not null,
five_grid_analysis_di varchar(255) not null,
five_grid_analysis_wai varchar(255) not null,
five_grid_analysis_zong varchar(255) not null,
verse varchar(100) not null,
sexual_id int not null,
foreign key(sexual_id) references sexual(id)
);


create table sexual(
id int auto_increment primary key,
sexual varchar(10) not null
);
