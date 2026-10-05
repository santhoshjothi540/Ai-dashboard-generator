import pandas as pd


def load_data(uploaded_file):
    """
    Load CSV or Excel file into a Pandas DataFrame.

    Improvements over the original version:
        - Supports .csv, .xlsx, and .xls (matching the file types already
          accepted by the uploader in app.py).
        - Falls back to a Latin-1 decode if a CSV isn't valid UTF-8.
        - Validates that the file actually contains columns and rows.
        - Raises clear, descriptive ValueError messages instead of raw
          pandas exceptions, so the UI can show a useful error to the user.

    The returned DataFrame's contents are never modified or filtered —
    only load/validate/error-handle behavior has changed.
    """

    if uploaded_file is None:
        return None

    file_name = getattr(uploaded_file, "name", "") or ""
    file_name_lower = file_name.lower().strip()

    if not file_name_lower:
        raise ValueError("The uploaded file has no name and cannot be identified.")

    # Reset the file pointer in case it was read before reaching this point.
    try:
        uploaded_file.seek(0)
    except (AttributeError, OSError):
        pass

    # ------------------------------------------------------------------
    # CSV
    # ------------------------------------------------------------------
    if file_name_lower.endswith(".csv"):

        try:
            df = pd.read_csv(uploaded_file)

        except UnicodeDecodeError:
            try:
                uploaded_file.seek(0)
            except (AttributeError, OSError):
                pass
            try:
                df = pd.read_csv(uploaded_file, encoding="latin1")
            except Exception as error:
                raise ValueError(
                    f"'{file_name}' could not be decoded as UTF-8 or Latin-1: {error}"
                )

        except pd.errors.EmptyDataError:
            raise ValueError(f"'{file_name}' is empty and contains no data.")

        except pd.errors.ParserError as error:
            raise ValueError(
                f"'{file_name}' could not be parsed as a valid CSV file: {error}"
            )

        except Exception as error:
            raise ValueError(f"Failed to read '{file_name}' as CSV: {error}")

    # ------------------------------------------------------------------
    # Excel (.xlsx / .xls)
    # ------------------------------------------------------------------
    elif file_name_lower.endswith((".xlsx", ".xls")):

        try:
            df = pd.read_excel(uploaded_file)

        except ValueError as error:
            raise ValueError(
                f"'{file_name}' could not be read as a valid Excel file: {error}"
            )

        except ImportError as error:
            raise ValueError(
                f"Missing dependency required to read '{file_name}': {error}"
            )

        except Exception as error:
            raise ValueError(f"Failed to read '{file_name}' as Excel: {error}")

    # ------------------------------------------------------------------
    # Unsupported format
    # ------------------------------------------------------------------
    else:
        raise ValueError(
            f"Unsupported file format '{file_name}'. "
            "Please upload a CSV or Excel (.xlsx, .xls) file."
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    if df is None:
        raise ValueError(f"'{file_name}' could not be loaded into a DataFrame.")

    if df.shape[1] == 0:
        raise ValueError(f"'{file_name}' does not contain any columns.")

    if df.shape[0] == 0:
        raise ValueError(f"'{file_name}' does not contain any data rows.")

    return df
