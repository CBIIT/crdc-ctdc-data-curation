
# Task 1: Name File Change

## Overview 
With the existing names applied to the CMB-derived data files inclusive of repetitive and unnecessary/confusing "annotations"
all such files in our current inventory should be renamed according to the following naming convention,
such that when displayed within the CTDC UI their origins and derivation are immediately clear to end users.


## Action Item

For the unfiltered Oncomine variant analysis .vcf files:
Change file names resembling "MSB-00140-06_v1_MSB-00140-06_RNA_v1_Non-Filtered_Copy.vcf"
to "MSB-00140-06-somatic-mutations-CTDCv1.vcf"


For the validated Oncomine-derived variant analysis .pdf files:
Change file names resembling "MSB-00140-06_v1_MSB-00140-06_RNA_v1_Non-Filtered_OR_(3)-Copy.pdf
to "MSB-00140-06-genomic-report-CTDCv1.pdf"


# Task 2 : Create File Transfer Manifest


## Overview 
With all CMB data files in previous steps already renamed, create File Transfer Manifests inclusive of all such CMB data in support of the simultaneous:

## Goal
Transfer of the files in question to their final S3 storage locations
Generation of the corresponding DCF indexing manifests
Generation of the corresponding data file metadata file via which records about the existence and location of the data files themselves can be loaded into the underlying CTDC database
 
## Action Item

The File Transfer Manifests created must also annotate the various data file records as follows:
 
For files that have been renamed such that their newly-assigned file names contain the term "somatic-mutations":

- Assign a value of "data_file" to each file and report it in the "type" column of the File Transfer Manifest
- Report the name of the file, inclusive of its file extension, in the "data_file_name" column
- Extract the first 13 characters of the filename, which represent the CMB Biospecimen ID, and report it in the "specimen.specimen_id" column, in order to identify the specimen (CTDC Biospecimen) to which the file pertains
- Assign a value of "Variant Call File" to each file, and report it in the "data_file_type" column
- Assign a value of "Unfiltered Oncomine variant analysis" to each file, and report it in the the "data_file_description" column
- Assign a value of "md5sum" to each file, and report it in the "data_file_checksum_type" column
- Assign a value of "Uncompressed" to each file, and report it in the "data_file_compression_status" column
- Calculate the exact size of each file, and report the value in the "data_file_size" column
- Calculate the md5sum value of each file, and report the value in the "data_file_checksum_value" column
 
 
For files that have been renamed such that their newly-assigned file names contain the term "genomic-report":

- Assign a value of "data_file" to each file and report it in the "type" column of the File Transfer Manifest
- Report the name of the file, inclusive of its file extension, in the "data_file_name" column
- Extract the first 13 characters of the filename, which represent the CMB Biospecimen ID, and report it in the "specimen.specimen_id" column, in order to identify the specimen (CTDC Biospecimen) to which the file pertains
- Assign a value of "Variant Report" to each file, and report it in the "data_file_type" column
- Assign a value of "Validated Oncomine-derived variant analysis" to each file, and report it in the the "data_file_description" column
- Assign a value of "md5sum" to each file, and report it in the "data_file_checksum_type" column
- Assign a value of "Uncompressed" to each file, and report it in the "data_file_compression_status" column
- Calculate the exact size of each file, and report the value in the "data_file_size" column
- Calculate the md5sum value of each file, and report the value in the "data_file_checksum_value" column
 
 
For files that have been renamed such that their newly-assigned file names contain the term "clinical-report":

- Assign a value of "data_file" to each file and report it in the "type" column of the File Transfer Manifest
- Report the name of the file, inclusive of its file extension, in the "data_file_name" column
- Extract the first 9 characters of each filename, which represent the CMB Participant ID, and report it in the "subject.subject_id" column, in order to identify the subject (CTDC Participant) to which the file pertains
- Assign a value of "Clinical Report" to each file, and report it in the "data_file_type" column
- Assign a value of "Detailed clinical evaluation" to each file, and report it in the the "data_file_description" column
- Assign a value of "md5sum" to each file, and report it in the "data_file_checksum_type" column
- Assign a value of "Uncompressed" to each file, and report it in the "data_file_compression_status" column
- Calculate the exact size of each file, and report the value in the "data_file_size" column
- Calculate the md5sum value of each file, and report the value in the "data_file_checksum_value" column




# Source

https://tracker.nci.nih.gov/browse/CTDC-1365

https://tracker.nci.nih.gov/browse/CTDC-1364
