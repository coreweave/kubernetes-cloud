PROGRAM compiler_wrapper
    ! Wraps GCC invocations,
    ! replacing -D__AVX512__ and -D__SCALAR__ preprocessor definitions
    ! with -D__AVX256__, and -march=native with -march=skylake,
    ! for better reproducibility and compatibility.
    IMPLICIT NONE
    INTEGER :: i, exitcode = 0, full_length = 0, truncated = 0
    CHARACTER(len=:), ALLOCATABLE :: arg, command
    ALLOCATE(CHARACTER(len=128) :: arg)
    command = "gcc"

    DO i = 1, COMMAND_ARGUMENT_COUNT()
        DO
            CALL GET_COMMAND_ARGUMENT(i, arg, full_length, truncated)
            IF (truncated == 0) THEN
                EXIT
            ELSEIF (truncated == -1) THEN
                DEALLOCATE(arg)
                ALLOCATE(CHARACTER(len=full_length) :: arg)
            ELSE
                CALL EXIT(95)
            END IF
        END DO
        IF (arg == "-march=native") THEN
            command = command // " '-march=skylake'"
        ELSEIF (arg == "-D__AVX512__" .OR. arg == "-D__SCALAR__") THEN
            command = command // " '-D__AVX256__'"
        ELSE
            command = command // shell_escaped(arg)
        END IF
    END DO
    CALL SYSTEM(command, exitcode)
    IF (exitcode > 255) THEN
        exitcode = MAX(IAND(exitcode, 255), 1)
    ENDIF
    CALL EXIT(exitcode)


    CONTAINS
        FUNCTION shell_escaped(str) result(out)
            ! Turns [str] into [ 'str'] and replaces all
            ! internal ['] characters with ['"'"']
            IMPLICIT NONE
            CHARACTER(len=*), INTENT(IN) :: str
            CHARACTER(len=:), ALLOCATABLE :: out
            INTEGER :: i, out_i, old_len, out_len

            old_len = LEN_TRIM(str)
            ! Figure out the new length to allocate by scanning `str`.
            ! This always needs to add at least [ '] at the beginning
            ! and ['] at the end, so the length increases by at least 3.
            out_len = old_len + 3
            DO i = 1, old_len
                IF (str(i:i) == "'") THEN
                    out_len = out_len + 4
                END IF
            END DO
            ALLOCATE(CHARACTER(len=out_len) :: out)

            ! Copy over the string, performing necessary escapes.
            out(1:2) = " '"
            out_i = 3
            DO i = 1, old_len
                IF (str(i:i) == "'") THEN
                    ! Escape internal single-quotes
                    out(out_i:out_i + 4) = '''"''"'''
                    out_i = out_i + 5
                ELSE
                    ! No escaping needed
                    out(out_i:out_i) = str(i:i)
                    out_i = out_i + 1
                END IF
            END DO
            out(out_i:out_i) = "'"
        END FUNCTION
END PROGRAM
