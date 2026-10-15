from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


class DateShiftProcessor:
    """
    Scales dates by a defined offset.
    """

    def __init__(
        self,
        date_offset: relativedelta,
        operation: str = "add",
        date_format: str = "%Y-%m-%d",
    ):
        """
        Initialize the DateShiftProcessor.

        Args:
            date_offset: a date offset to apply to all dates.
            operation:denotes whether the offset is added/subtracted from the original date.
            date_format: a python date code used to format the outputted dates.
        """
        # validate operation values
        valid_operations = ["add", "subtract"]
        if operation.lower() in valid_operations:
            self._operation = operation.lower()
        else:
            raise ValueError(
                f"The operation {operation} does not exist. Unable to initialize DateShiftProcessor."
            )
        # initialize offset and date formats
        self._offset = date_offset
        self._date_format = date_format

    def __call__(self, entity: dict) -> str:
        """
        Process date entities by shifting them forward or backwards by a given factor

        Args:
            entity: an individual entity returned by the DEID container.

        Examples:
            >>> text = ["today is 1990-01-01."]
            >>> request = {
                "text": text,
                "entity_detection": {
                    "accuracy": "high",
                    "entity_types": [
                        {
                        "type": "ENABLE",
                        "value": ["DATE", "DATE_OF_DEATH", "DOB"]
                        }
                        ],
                    },
                }
            >>> text_request = AnalyzeTextRequest.from_dict(request)
            >>> # run analyze text
            >>> resp = client.analyze_text(text_request)
            >>> # run post-processing tasks
            >>> entity_processors = {"DATE": DateShiftProcessor(date_offset=relativedelta(months=3)}
            >>> anon_text_blocks = deidentify_text(
                    text,
                    resp,
                    entity_processors=entity_processors,
                    default_processor=MarkerEntityProcessor()
                )
            >>> anon_text_blocks
                ["today is 1990-04-01."]
        """
        # iso-8601 format: date as year-month-day
        iso_date_str = entity["analysis_result"].get("formatted")
        date_obj = datetime.fromisoformat(iso_date_str)

        # select the operation
        if self._operation == "add":
            new_date = date_obj + self._offset
        else:
            new_date = date_obj - self._offset
        return f"{new_date.strftime(self._date_format)}"


class DateBucketProcessor:
    """
    Bin date entities into defined buckets.
    """

    def __init__(self, date_bin: str, date_format: str = "%Y-%m-%d"):
        """
        Initialize the DateBucketProcessor.

        Args:
            date_bins: date compnents used to bin detected date entities. Acceptable values include "decade",
                "year", and "month".
            date_format: a python date code used to format the outputted dates.
        """
        # check for valid bin values
        valid_date_bins = ["decade", "year", "month"]
        if date_bin.lower() in valid_date_bins:
            self._date_bin = date_bin.lower()
        else:
            raise ValueError(
                f"date_bin value: {date_bin} is not a valid value. Unable to initialize DateBucketProcessor."
            )
        # initialize date formats
        self._date_format = date_format

    def __call__(self, entity: dict) -> str:
        """
        Process date entities by binning them into date buckets

        Args:
            entity: an individual entity returned by the DEID container.

        Examples:
            >>> text = ["today is 1990-01-01."]
            >>> request = {
                "text": text,
                "entity_detection": {
                    "accuracy": "high",
                    "entity_types": [
                        {
                        "type": "ENABLE",
                        "value": ["DATE", "DATE_OF_DEATH", "DOB"]
                        }
                        ],
                    },
                }
            >>> text_request = AnalyzeTextRequest.from_dict(request)
            >>> # run analyze text
            >>> resp = client.analyze_text(text_request)
            >>> # run post-processing tasks
            >>> entity_processors = {"DATE": DateBucketProcessor(date_bin="year")}
            >>> anon_text_blocks = deidentify_text(
                    text,
                    resp,
                    entity_processors=entity_processors,
                    default_processor=MarkerEntityProcessor()
                )
            >>> anon_text_blocks
                ["today is between 1990-01-01 and 1990-12-31."]
        """
        # iso-8601 format: date as year-month-day
        iso_date_str = entity["analysis_result"].get("formatted")
        date_obj = datetime.fromisoformat(iso_date_str)

        # start period
        if self._date_bin == "decade":
            decade_date_yr = (date_obj.year // 10) * 10
            strt_date = datetime(decade_date_yr, 1, 1)
        elif self._date_bin == "year":
            strt_date = date_obj.replace(month=1, day=1)
        else:
            # monnth
            strt_date = date_obj.replace(day=1)

        # end period
        if self._date_bin == "decade":
            end_date = (strt_date + relativedelta(years=10)) - timedelta(days=1)
        elif self._date_bin == "year":
            end_date = (strt_date + relativedelta(years=1)) - timedelta(days=1)
        else:
            # monnth
            end_date = (strt_date + relativedelta(months=1)) - timedelta(days=1)
        return f"[{strt_date.strftime(self._date_format)} to {end_date.strftime(self._date_format)}]"


class DateComponentProcessor:
    """
    Redact select part of a date.
    """

    def __init__(self, redact_components: list[str]):
        """
        initialize the  DateComponentProcessor

        Args:
            redact_component: the date compnents that need to be redacted.
        """
        # valid date redacted date components
        valid_date_comps = ["DAY", "MONTH", "YEAR"]
        for date_comp in redact_components:
            if date_comp.upper() not in valid_date_comps:
                raise ValueError(
                    f"{date_comp} element in redact_component is not valid."
                )
        self._redact_components = redact_components

    def __call__(self, entity: dict) -> str:
        """
        Process date entities by selectively redacting certain components from a date.

        Args:
            entity: an individual entity returned by the DEID container.

        Examples:
        """
        offset = entity["location"]["stt_idx"]
        text = entity["text"]
        for subtype in entity["analysis_result"]["subtypes"]:
            if subtype["label"] in self._redact_components and "location" in subtype:
                stt = subtype["location"]["stt_idx"] - offset
                end = subtype["location"]["end_idx"] - offset
                text = text[:stt] + "#" * (end - stt) + text[end:]
        return text
