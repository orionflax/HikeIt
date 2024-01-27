@Dao
public interface FormEntryDao {
    @Query("SELECT * FROM formEntry")
    List<FormEntry> getAll();

    @Insert
    void insertAll(FormEntry... formEntries);
}