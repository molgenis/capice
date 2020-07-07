package org.molgenis.capice.vcf;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;

import org.apache.commons.csv.CSVRecord;
import org.junit.jupiter.api.Test;

class TsvRecordComparatorTest {

  @Test
  void compareEqual() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("1_12345_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("1_12345_A_T").when(csvRecord2).get(0);
    assertEquals(0,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void compareChrom1() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("1_12345_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("22_12345_A_T").when(csvRecord2).get(0);
    assertEquals(-21,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void compareChrom2() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("22_12345_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("1_123456_A_T").when(csvRecord2).get(0);
    assertEquals(21,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void compareChrom3() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("1_12345_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("Y_12345_A_T").when(csvRecord2).get(0);
    assertEquals(-1,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void compareChrom4() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("MT_12345_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("Y_12345_A_T").when(csvRecord2).get(0);
    assertEquals(1,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void comparePos1() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("1_12346_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("1_12345_A_T").when(csvRecord2).get(0);
    assertEquals(1,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void comparePos2() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("1_12345_A_T").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    doReturn("1_1234678_A_T").when(csvRecord2).get(0);
    assertEquals(-1222333,comparator.compare(csvRecord1, csvRecord2));
  }

  @Test
  void compareIllegal() {
    TsvRecordComparator comparator = new TsvRecordComparator();
    CSVRecord csvRecord1 = mock(CSVRecord.class);
    doReturn("1_12345_AT").when(csvRecord1).get(0);
    CSVRecord csvRecord2 = mock(CSVRecord.class);
    assertThrows(PositionParseException.class , () ->comparator.compare(csvRecord1, csvRecord2));
  }
}