import pandas as pd
import os

# Define data directory
data_dir = "data"

# List of CSV files to analyze
csv_files = [
    "jobsandskills-Job Role_CWF_KT.csv",
    "jobsandskills-Job Role_TCS_CCS.csv",
    "jobsandskills-TSC_CCS_K_A_1.csv",
    "jobsandskills-TSC_CCS_K_A_2.csv",
    "jobsandskills-TSC_CCS_K_A_3.csv",
    "jobsandskills-TSC_CCS_K_A_4.csv",
    "jobsandskills-TSC_CCS_K_A_5.csv",
    "jobsandskills-TSC_CCS_K_A_6.csv",
    "jobsandskills-TSC_CCS_K_A_7.csv",
    "jobsandskills-TSC_CCS_K_A_8.csv",
    "jobsandskills-TSC_CCS_Key.csv"
]

print("=== CSV Schema Analysis for RAG Design ===\n")

for csv_file in csv_files:
    file_path = os.path.join(data_dir, csv_file)
    print(f"\n{'='*60}")
    print(f"File: {csv_file}")
    print('='*60)
    
    try:
        # Read CSV with different encodings if needed
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_csv(file_path, encoding='latin-1')
        
        print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"\nColumns ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        print(f"\nData Types:")
        for col, dtype in df.dtypes.items():
            print(f"  - {col}: {dtype}")
        
        print(f"\nFirst 3 rows preview:")
        print(df.head(3).to_string())
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            print(f"\nNull values:")
            for col, count in null_counts[null_counts > 0].items():
                print(f"  - {col}: {count} ({count/len(df)*100:.1f}%)")
        
        # Sample unique values for key columns
        print(f"\nSample unique values (first 5):")
        for col in df.columns[:3]:  # Show first 3 columns
            unique_vals = df[col].dropna().unique()[:5]
            print(f"  - {col}: {list(unique_vals)}")
            
    except Exception as e:
        print(f"Error reading file: {e}")

print("\n\n=== Schema Analysis Summary ===")
print("""
Based on the schema analysis, here's the data structure for RAG implementation:

1. **Job Role Files (CWF_KT, TCS_CCS)**:
   - Contains job role information and mappings
   - Key fields likely include job titles, codes, descriptions
   
2. **TSC_CCS Files (K_A_1 through K_A_8)**:
   - Technical Skills Competency data
   - Appears to be segmented across multiple files
   - Contains skill categories, competencies, and assessments
   
3. **TSC_CCS_Key File**:
   - Likely contains key/legend for interpreting TSC codes
   - Maps codes to descriptions or categories

For RAG implementation, we'll need to:
- Create embeddings for job roles and their descriptions
- Index technical skills and competencies
- Build relationships between jobs and required skills
- Enable semantic search across all dimensions
""")
