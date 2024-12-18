# load data manipulation packages
import pandas as pd
import numpy as np

# load data visualization packages
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

"""##IMPORT DATA"""

# read data
df = pd.read_csv('Clean_Dataset.csv')

import pandas as pd
import numpy as np

# Load your dataset
df = pd.read_csv('Clean_Dataset.csv')

# Simulate Departure Dates (e.g., random dates between a range)
df['Departure_Date'] = pd.to_datetime(np.random.choice(pd.date_range('2023-12-01', '2024-01-31'), len(df)))

# Preview the dataset with the new column
print(df[['Departure_Date']].head())

# drop duplicates
 df = df.drop_duplicates()

df.head()

# sanity check
print(f'Number of duplicated data: {df.duplicated().sum()}')

# drop unnecessary column
df = df.drop(columns = ['flight'])

# check data shape
df.shape

# check number of missing values
df.isnull().sum() / len(df) * 100

# check data types
df.dtypes

"""## Data Splitting"""

def split_input_output(data, target_column):
 #split the data into features and target variable
    X = data.drop(columns = target_column)
    y = data[target_column]

    return X, y

X, y = split_input_output(data = df,
                          target_column = 'price')

X.head()

y.head()

from sklearn.model_selection import train_test_split

# splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size = 0.2,
                                                    random_state = 123)

# getting the number of samples and features from the training set
n_samples, n_features = X_train.shape

print(f'Number of samples: {n_samples}')
print(f'Number of features: {n_features}')

"""##EXPLORATORY DATA ANALYSIS"""

# concatenating the training and test set for eda
df_eda = pd.concat([X_train, y_train], axis=1)
df_eda.head()

num_column = df_eda.select_dtypes(include='number').columns
cat_column = df_eda.select_dtypes(include='object').columns

print(f'List numerical columns: \n{num_column}')
print(f'\nList categorical columns: \n{cat_column}')

"""###Checking for missing values

"""

# checking missing values
df_eda.isnull().sum() / len(df_eda)

"""###Checking Unique Values"""

# iterating through categorical column to check unique values
for i in cat_column:
    print(f'Unique value in {i} column:')
    print(df_eda[i].unique())
    print('-'*100)

"""###Descriptive Analysis"""

# check descriptive data
df_eda.describe()

"""###Univariate Analysis"""

# creating subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# looping through numerical column to create distribution plot
for i in range(0, len(num_column)):
    sns.distplot(df_eda[num_column[i]], ax=ax[i])
    ax[i].set_title(num_column[i])
    ax[i].set_xlabel('')

plt.tight_layout()
plt.show()

# creating subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# looping through numerical column to create box plot
for i in range(0, len(num_column)):
    sns.boxplot(x = df_eda[num_column[i]], ax=ax[i], palette='muted')
    ax[i].set_title(num_column[i])
    ax[i].set_xlabel('')

plt.tight_layout()
plt.show()

# list of categorical columns to be visualized
list_col = ['airline', 'class', 'source_city',
            'destination_city', 'departure_time', 'arrival_time']
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(18,10))
ax = ax.flatten()

# looping through categorical column to create count plot
for i in range(len(list_col)):
    # get the order of categories based on frequency
    order = df_eda[list_col[i]].value_counts().index

    sns.countplot(x = df_eda[list_col[i]],
                  ax=ax[i],
                  order=order,
                  palette = 'coolwarm')
    ax[i].set_title(list_col[i])
    ax[i].set_xlabel('')

plt.tight_layout()
plt.show()

"""###Bivariate Analysis"""

# calculate and sort the airlines based on median price
median_price_airline = df_eda.groupby('airline')['price'].median().reset_index()
sorted_airline = median_price_airline.sort_values(by='price', ascending=False)

# create subplots
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,6))
plt.suptitle('Airlines with The Most Expensive Flight Fare',fontsize=16)

# bar plot for median flight prices by airline
sns.barplot(data=sorted_airline,
            x='airline',
            y='price',
            palette = 'coolwarm',
            ax = ax[0])
ax[0].set_xlabel('airline')
ax[0].set_ylabel('flight fare')

# box plot for median flight prices by airline
sns.boxplot(data=df_eda,
            x='airline',
            y='price',
            palette = 'coolwarm',
            ax = ax[1])
ax[1].set_xlabel('airline')
ax[1].set_ylabel('flight fare')

plt.tight_layout()
plt.show()

# calculate and sort business class airlines based on median price
airline_business = df_eda[df_eda['class'] == 'Business']
business_price = airline_business.groupby('airline')['price'].median().reset_index()
sorted_business_price = business_price.sort_values(by = 'price', ascending=False)

# calculate and sort economy class airlines based on median price
airline_economy = df_eda[df_eda['class'] == 'Economy']
economy_price = airline_economy.groupby('airline')['price'].median().reset_index()
sorted_economy_price = economy_price.sort_values(by = 'price', ascending=False)

# create subplots
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,6))
plt.suptitle('Flight Fare based on Airline and Class', fontsize=16)

# bar plot for median flight prices for business Class
sns.barplot(data = sorted_business_price,
            x='airline',
            y='price',
            palette = 'coolwarm',
            ax = ax[0])
ax[0].set_title('Business Class')
ax[0].set_xlabel('airline')
ax[0].set_ylabel('price')

# bar plot for median flight prices for economy Class
sns.barplot(data = sorted_economy_price,
            x='airline',
            y='price',
            palette = 'coolwarm',
            ax = ax[1])
ax[1].set_title('Economy Class')
ax[1].set_xlabel('airline')
ax[1].set_ylabel('price')

plt.tight_layout()
plt.show()

# define the list of categorical columns
barchart_list = ['class', 'stops', 'departure_time',
                'arrival_time', 'source_city', 'destination_city']

# create subplots
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(18,10))
ax = ax.flatten()

# loop through each category in the barchart_list
for i, bar in enumerate(barchart_list):
    flight_fare = df_eda.groupby(bar)['price'].median().reset_index()
    sorted_categories = flight_fare.sort_values(by = 'price', ascending=False)

    # create a bar plot for each category
    sns.barplot(data=sorted_categories,
                y = bar,
                x ='price',
                palette = 'coolwarm',
                ax = ax[i])

    # set the title and labels for each subplot
    ax[i].set_title(f'Price by {bar}', fontsize=14)
    ax[i].set_xlabel('Price')
    ax[i].set_ylabel('')

plt.tight_layout()
plt.show()

# define the columns to plot.
cols = ['duration', 'days_left']
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,6))

# loop through the columns and create scatter plots
for i in range(len(cols)):
    sns.scatterplot(data = df_eda,
                    x = cols[i],
                    y = 'price',
                    hue = 'class',
                    ax = ax[i],
                    palette = 'muted')
    ax[i].set_title(f'Price by {cols[i]}')
    ax[i].set_xlabel(cols[i])

plt.tight_layout()
plt.show()

# Classify bookings as "Last Minute" or "Early Bird"
def classify_booking_type(df):
    conditions = [
        (df['days_left'] <= 7),  # Last Minute: <= 7 days left
        (df['days_left'] >= 30)  # Early Bird: >= 30 days left
    ]
    choices = ['Last Minute', 'Early Bird']
    df['Booking_Type'] = np.select(conditions, choices, default='Normal')  # Default: Normal
    return df

# Apply the function to the dataset
df = classify_booking_type(df)

# Preview the updated dataset
print(df[['days_left', 'Booking_Type']].head())

"""##PREPROCESSING"""

# concatenate X_train and y_train for preprocessing
train_set = pd.concat([X_train, y_train], axis=1)

"""###Handling Outliers

"""

# fliter data for outlier checking
train_set[train_set['duration'] > 24]

def remove_outlier(data, columns):
  # create a copy of the original data
    clean_data = data.copy()

    # iterate through the specified columns to remove outliers
    for col in columns:
        Q1 = np.quantile(data[col], 0.25)
        Q3 = np.quantile(data[col], 0.75)
        IQR = Q3 - Q1
        upper_thres = 1.5 * IQR
        lower_thres = -1.5 * IQR

        clean_data[col] = clean_data[col][(clean_data[col] >= lower_thres)
                                          & (clean_data[col] <= upper_thres)]

    # drop any rows with NaN values
    clean_data = clean_data.dropna()

    return clean_data

# Remove outliers from the duration column
train_set_clean = remove_outlier(data = train_set, columns = ['duration'])

# creating subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# looping through numerical column to create distribution plot
for i in range(0, len(num_column)):
    sns.distplot(train_set_clean[num_column[i]], ax=ax[i])
    ax[i].set_title(num_column[i])
    ax[i].set_xlabel('')

plt.tight_layout()
plt.show()

# creating subplots
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# looping through numerical column to create box plot
for i in range(0, len(num_column)):
    sns.boxplot(x = train_set_clean[num_column[i]], ax=ax[i], palette='muted')
    ax[i].set_title(num_column[i])
    ax[i].set_xlabel('')

plt.tight_layout()
plt.show()

print(f'Shape data sebelum drop outlier: {train_set.shape}')
print(f'Shape data sebelum drop outlier: {train_set_clean.shape}')

percent_outlier = (1 - (len(train_set_clean) / len(train_set))) * 100
print(f'Persentase data yang dihapus: {round(percent_outlier, 2)}%')

# create subplots
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,6))
cols = ['duration', 'days_left']

# loop through the specified columns and create scatter plots
for i in range(len(cols)):
    sns.scatterplot(data = train_set_clean,
                    x = cols[i],
                    y = 'price',
                    hue = 'class',
                    ax = ax[i],
                    palette = 'muted')
    ax[i].set_title(f'Price by {cols[i]}')
    ax[i].set_xlabel(cols[i])

plt.tight_layout()
plt.show()

"""###Categorical Encoding"""

from sklearn.preprocessing import OneHotEncoder

def categorical_encoding(data, fit=True, encoder=None):
  # create a copy of the original data and reset the index
    data_copy = data.copy().reset_index(drop=True)
    target_col = data_copy['price']
    data_copy = data_copy.drop('price', axis=1)

    # select categorical features
    cat_features = data_copy.select_dtypes(include='object').columns

    if fit:
        # initialize OneHotEncoder
        ohe = OneHotEncoder(handle_unknown='ignore', drop='first')

        # fit and transform the categorical features
        ohe.fit(data_copy[cat_features])
        encoder = ohe
        encoded_df = pd.DataFrame(ohe.transform(data_copy[cat_features]).toarray())
    else:
      # use existing encoder object to transform
        encoded_df = pd.DataFrame(encoder.transform(data_copy[cat_features]).toarray())

    # rename columns
    encoded_df.columns = encoder.get_feature_names_out(cat_features)

    # drop original cat feature
    dropped_data = data_copy.drop(cat_features, axis=1)

    # merge one-hot encoded columns back with original DataFrame
    final_df = dropped_data.join([encoded_df, target_col])

    return encoder, final_df

encoder, train_set_clean = categorical_encoding(data = train_set_clean,
                                                fit = True)

train_set_clean.head()

train_set_clean.columns

"""###Correlation Test"""

def plot_corr_heatmap(data):
  # define the figure
    plt.figure(figsize=(12, 12))

    # plot correlation heatmap
    sns.heatmap(data.corr(),
                cmap='Blues',
                annot = False)

# Plot the correlation heatmap
plot_corr_heatmap(data = train_set_clean)

X_train, y_train = split_input_output(data = train_set_clean,
                                      target_column = 'price')

"""###Standardization"""

from sklearn.preprocessing import StandardScaler

def fit_scaler(data):
  # initialize the StandardScaler
    scaler = StandardScaler()

    # fit the scaler to the data
    scaler.fit(data)

    return scaler

def transform_scaler(data, scaler):
  # Transform the data using the fitted scaler
    df_scaled = pd.DataFrame(scaler.transform(data))

    # Set the index and columns of the scaled DataFrame
    df_scaled.index = data.index
    df_scaled.columns = data.columns

    print(f'Data shape: {data.shape}')

    return df_scaled

# fit scaler using df_rfm_data data
scaler = fit_scaler(data = X_train)

# transform scaler using df_rfm_data data
X_scaled = transform_scaler(data = X_train,
                            scaler = scaler)

X_scaled.head()

"""###Feature Selection"""

from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

def feature_selection(estimator, X_train, y_train):
  # fit the model
    estimator.fit(X_train, y_train)

    # predict
    y_pred_train = estimator.predict(X_train)
    train_score = mean_squared_error(y_true=y_train, y_pred=y_pred_train)

    # cross validation
    valid_scores = cross_val_score(estimator=estimator,
                                   X=X_train,
                                   y=y_train,
                                   cv=5,
                                   scoring='neg_mean_squared_error')
    cv_score = -np.mean(valid_scores)

    # extract coefficient
    coef_ = estimator.coef_
    intercept_ = estimator.intercept_
    estimator_params = np.append(coef_, intercept_)

    # create DataFrame for coefficients
    estimator_params_df = pd.DataFrame(estimator_params,
                                       index=list(X_train.columns) + ['constant'],
                                       columns=['coefficient'])

    return estimator, train_score, cv_score, estimator_params_df

alpha = np.linspace(0, 10, 100)

# To store results
mse_train_list = []
mse_cv_list = []
model_list = []

# Loop over different alpha values
for i in alpha:
    model_i, train_score_i, \
        cv_score_i, model_param_i = feature_selection(estimator=Lasso(alpha=i),
                                                      X_train=X_scaled,
                                                      y_train=y_train)

    mse_train_list.append(train_score_i)
    mse_cv_list.append(cv_score_i)
    model_list.append(model_param_i)

# create subplots
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,6))

# plot error
ax.plot(alpha, mse_train_list, c='r', marker='.', label='Train')
ax.plot(alpha, mse_cv_list, c='g', marker='.', label='CV')
ax.set_xlabel('alpha')
ax.set_ylabel('MSE')

plt.grid()
plt.legend()
plt.show()

# find the index of the minimum cross-validated mse
best_index = np.argmin(mse_cv_list)

# retrieve the best alpha value and corresponding cross-validated mse
best_alpha = alpha[best_index]
best_lasso_cv = mse_cv_list[best_index]

# Output the best alpha value and the corresponding cross-validated mse
best_alpha, best_lasso_cv

# best model
best_model_lasso = model_list[best_index]
best_model_lasso

from statsmodels.stats.outliers_influence import variance_inflation_factor

def calculate_vif(data):
  # create an empty DataFrame to store VIF data
    vif_data = pd.DataFrame()
    vif_data['feature'] = data.columns

    # calculate VIF for each feature using the variance_inflation_factor function
    vif_data['VIF'] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]

    return vif_data

    # calculate VIF on the scaled features
df_vif = calculate_vif(X_scaled)
df_vif



# Categorize prices into three tiers
def categorize_prices(df):
    # Compute quantiles
    low_threshold = df['price'].quantile(0.33)
    high_threshold = df['price'].quantile(0.66)

    # Assign categories based on thresholds
    conditions = [
        (df['price'] <= low_threshold),  # Low prices
        (df['price'] > low_threshold) & (df['price'] <= high_threshold),  # Moderate prices
        (df['price'] > high_threshold)  # High prices
    ]
    choices = ['Green', 'Yellow', 'Red']
    df['Price_Category'] = np.select(conditions, choices, default='Yellow')  # Default: Moderate
    return df

# Apply the function to the  dataset
df = categorize_prices(df)
predicted_df = pd.DataFrame({'price': df['price']})

# Now you can categorize the predicted prices
predicted_df = categorize_prices(predicted_df)

# Preview the updated dataset
print(df[['price', 'Price_Category']].head()) # Corrected column name to Price_Category
print(predicted_df[['price', 'Price_Category']].head()) # Print predicted data as well

def assign_price_category(price):
    # Define high_threshold and low_threshold within the function or before calling it
    high_threshold = 10000  # Example value, adjust as needed
    low_threshold = 5000   # Example value, adjust as needed

    if price > high_threshold:
        return 'Red'
    elif price > low_threshold:
        return 'Yellow'
    else:
        return 'Green'

df['Price_Category'] = df['price'].apply(assign_price_category)

import matplotlib.pyplot as plt
import calendar
from matplotlib.patches import Circle, Patch

# Function to create a calendar visualization with prices and colored circles
def plot_price_calendar_with_details(df, year, month):
    # Ensure 'Departure_Date' is in datetime format
    df['Departure_Date'] = pd.to_datetime(df['Departure_Date'])

    # Filter data for the specified month and year
    month_data = df[(df['Departure_Date'].dt.year == year) & (df['Departure_Date'].dt.month == month)]

    # Create a calendar matrix
    cal = calendar.Calendar()
    days_matrix = cal.monthdayscalendar(year, month)

    # Create a mapping for colors
    color_map = {'Red': 'red', 'Yellow': 'yellow', 'Green': 'green'}

    # Plot the calendar
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(f"Flight Prices for {calendar.month_name[month]} {year}", fontsize=16)

    for i, week in enumerate(days_matrix):
        for j, day in enumerate(week):
            if day == 0:
                continue  # Skip empty days

            # Find the corresponding data for this day
            date_str = f"{year}-{month:02d}-{day:02d}"
            day_data = month_data[month_data['Departure_Date'].astype(str) == date_str]

            if not day_data.empty:
                price = day_data['Price'].values[0]  # Get the ticket price
                price_category = day_data['Price_Category'].values[0]  # Get the price category

                # Draw a circle with the appropriate color
                ax.add_patch(Circle((j, -i), 0.4, color=color_map[price_category], alpha=0.6))

                # Display the price along with the date
                ax.text(j, -i, f"{day}\n₹{price:.0f}", ha='center', va='center', fontsize=10, color='black')
            else:
                # Only display the date if no data is available
                ax.text(j, -i, str(day), ha='center', va='center', fontsize=12, color='gray')

    # Adjust axes
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-len(days_matrix) + 0.5, 0.5)
    ax.axis('off')

    # Add a legend
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='High Price'),
        Patch(facecolor='yellow', edgecolor='black', label='Moderate Price'),
        Patch(facecolor='green', edgecolor='black', label='Low Price')
    ]
    ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=12)

    plt.show()

# Example usage
plot_price_calendar_with_details(df, year=2024, month=11)

import matplotlib.pyplot as plt
import calendar
from matplotlib.patches import Circle, Patch

def plot_price_calendar_with_details(df, year, month):
    # Ensure 'Departure_Date' is in datetime format
    df['Departure_Date'] = pd.to_datetime(df['Departure_Date'])

    # Filter data for the specified month and year
    month_data = df[(df['Departure_Date'].dt.year == year) & (df['Departure_Date'].dt.month == month)]

    # Create a calendar matrix
    cal = calendar.Calendar()
    days_matrix = cal.monthdayscalendar(year, month)

    # Create a mapping for colors
    color_map = {'Red': 'red', 'Yellow': 'yellow', 'Green': 'green'}

    # Plot the calendar
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(f"Flight Prices for {calendar.month_name[month]} {year}", fontsize=16)

    for i, week in enumerate(days_matrix):
        for j, day in enumerate(week):
            if day == 0:
                continue  # Skip empty days

            # Find the corresponding data for this day
            date_str = f"{year}-{month:02d}-{day:02d}"
            day_data = month_data[month_data['Departure_Date'].astype(str) == date_str]

            if not day_data.empty:
                price = day_data['Price'].values[0]  # Get the ticket price
                price_category = day_data['Price_Category'].values[0]  # Get the price category

                # Draw a circle with the appropriate color
                circle = Circle((j, -i), 0.4, color=color_map[price_category], alpha=0.6)
                ax.add_patch(circle)

                # Display the price along with the date
                ax.text(j, -i, f"{day}\n₹{price:.0f}", ha='center', va='center', fontsize=10, color='black')
            else:
                # Only display the date if no data is available
                ax.text(j, -i, str(day), ha='center', va='center', fontsize=12, color='gray')

    # Adjust axes
    ax.set_xlim(-0.5, 6.5)  # Align the days horizontally
    ax.set_ylim(-len(days_matrix) + 0.5, 0.5)  # Align the weeks vertically
    ax.axis('off')  # Hide the axes

    # Add a legend
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='High Price'),
        Patch(facecolor='yellow', edgecolor='black', label='Moderate Price'),
        Patch(facecolor='green', edgecolor='black', label='Low Price')
    ]
    ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=12)

    plt.show()

# Example usage
plot_price_calendar_with_details(df, year=2024, month=11)

def assign_price_category(price):
    if price > 10000:  # High price threshold
        return 'Red'
    elif price > 5000:  # Moderate price threshold
        return 'Yellow'
    else:
        return 'Green'

df['Price_Category'] = df['price'].apply(assign_price_category)

"""##Modelling
###Baseline Model
"""

# calculate and print the baseline prediction
y_pred_baseline = np.mean(y_train)
print(f'Baseline prediction: {y_pred_baseline:.3f}')

from sklearn.metrics import mean_squared_error

def root_mean_square_error(y_true, y_pred):
  rmse = np.sqrt(mean_squared_error(y_true, y_pred))
  return rmse

rmse_baseline_train = root_mean_square_error(y_true = y_train,
                                             y_pred = np.ones(len(y_train)) * y_pred_baseline)

print(f'RMSE Baseline on training set: {rmse_baseline_train}')

# Categorize prices into three tiers
def categorize_prices(df):
    # Compute quantiles
    low_threshold = df['price'].quantile(0.33)
    high_threshold = df['price'].quantile(0.66)

    # Assign categories based on thresholds
    conditions = [
        (df['price'] <= low_threshold),  # Low prices
        (df['price'] > low_threshold) & (df['price'] <= high_threshold),  # Moderate prices
        (df['price'] > high_threshold)  # High prices
    ]
    choices = ['Green', 'Yellow', 'Red']
    df['Price_Category'] = np.select(conditions, choices, default='Yellow')  # Default: Moderate
    return df

# Apply the function to the  dataset
df = categorize_prices(df)
predicted_df = pd.DataFrame({'price': df['price']})

# Now you can categorize the predicted prices
predicted_df = categorize_prices(predicted_df)

# Preview the updated dataset
print(df[['price', 'Price_Category']].head()) # Corrected column name to Price_Category
print(predicted_df[['price', 'Price_Category']].head()) # Print predicted data as well

"""###Model Selection"""

from sklearn.metrics import r2_score

def fit_model(model, X_train, y_train):

    # fitting the model
    model.fit(X_train, y_train)

    # predict the model
    y_pred_train = model.predict(X_train)
    train_rmse = root_mean_square_error(y_true = y_train,
                                         y_pred = y_pred_train)

    # cross validation
    valid_score = cross_val_score(estimator = model,
                                  X = X_train,
                                  y = y_train,
                                  cv = 5,
                                  scoring = 'neg_mean_squared_error')
    cv_rmse = np.sqrt(-np.mean(valid_score))

    # calculate r2 score
    train_r2 = r2_score(y_train, y_pred_train)

    # store metrics
    metrics = pd.DataFrame({
        'Metrics' : ['RMSE Train', 'RMSE CV', 'R2 Score'],
        'Score' : [train_rmse, cv_rmse, train_r2]
    })

    return model, metrics

"""Linear Regression"""

# fit model with Linear Regression
from sklearn.linear_model import LinearRegression

model_lr, metrics_lr = fit_model(model = LinearRegression(),
                                 X_train = X_scaled,
                                 y_train = y_train)

metrics_lr

"""Random Forest"""

# fit model with Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor

model_rf, metrics_rf = fit_model(model = RandomForestRegressor(n_estimators=50,
                                                               random_state=123),
                                 X_train = X_train,
                                 y_train = y_train)
metrics_rf

"""XG BOOST"""

# fit model with XGBoost Regressor
from xgboost import XGBRegressor

model_xgb, metrics_xgb = fit_model(model = XGBRegressor(objective='reg:squarederror',
                                                        random_state = 123),
                                   X_train = X_scaled,
                                   y_train = y_train)
metrics_xgb

# create a dictionary to store the model evaluation metrics
model_results = {
    'Linear Regression': {
        'RMSE Train': 6821.15,
        'RMSE CV': 6822.38,
        'R2 Score': 0.9
    },
    'Random Forest': {
        'RMSE Train': 1143.17,
        'RMSE CV': 2670.19,
        'R2 Score': 0.99
    },
    'XGBoost': {
        'RMSE Train': 2934.87,
        'RMSE CV': 3015.62,
        'R2 Score': 0.98
    }}

# convert the model results dictionary into a pandas DataFrame
df_results = pd.DataFrame(model_results).T
df_results = df_results.reset_index().rename(columns={'index': 'Model'})
df_results

"""###Hyperparamete Tuning"""

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

# define the parameter distribution
param_dist = {
    'n_estimators' : randint(100, 300),
    'max_depth' : [None, 10, 20, 30, 40, 50],
    'min_samples_split' : randint(2, 11),
    'min_samples_leaf' : randint(1, 5),
    'max_features' : [1.0, 'auto', 'sqrt']
}

# initialize the Random Forest Regressor
model_rf = RandomForestRegressor(random_state=123, n_jobs = -1)

# initialize RandomizedSearchCV with the defined parameter distribution
random_search = RandomizedSearchCV(estimator = model_rf,
                                   param_distributions = param_dist,
                                   n_iter = 2,
                                   cv = 3,
                                   scoring = 'neg_mean_squared_error',
                                   verbose = 2,
                                   random_state = 123,
                                   n_jobs = -1)

# fit the RandomizedSearchCV model
random_search.fit(X_train, y_train)

# retrieve the best estimator found during the search
best_regressor = random_search.best_estimator_
best_regressor

"""##Evaluation"""

# fit the best model obtained from RandomizedSearchCV
model_best, metrics_best = fit_model(model = best_regressor,
                                     X_train = X_train,
                                     y_train = y_train)
metrics_best

# Categorize prices into three tiers
def categorize_prices(df):
    # Compute quantiles
    low_threshold = df['price'].quantile(0.33)
    high_threshold = df['price'].quantile(0.66)

    # Assign categories based on thresholds
    conditions = [
        (df['price'] <= low_threshold),  # Low prices
        (df['price'] > low_threshold) & (df['price'] <= high_threshold),  # Moderate prices
        (df['price'] > high_threshold)  # High prices
    ]
    choices = ['Green', 'Yellow', 'Red']
    df['price_category'] = np.select(conditions, choices, default='Yellow')  # Default: Moderate
    return df

# Apply the function to both current and predicted datasets
df = categorize_prices(df)
predicted_df = categorize_prices(predicted_df)

# Preview the updated dataset
print(df[['price', 'price_category']].head())

"""###Preprocessing Test Set"""

# concatenate the test features and target variable
test_set = pd.concat([X_test, y_test], axis=1)

# remove outliers from the duration column in the test dataset
test_set_clean = remove_outlier(data = test_set,
                                columns = ['duration'])

print(f'Shape data sebelum drop outlier: {test_set.shape}')
print(f'Shape data sebelum drop outlier: {test_set_clean.shape}')

percent_outlier = (1 - (len(test_set_clean) / len(test_set))) * 100
print(f'Persentase data yang dihapus: {round(percent_outlier, 2)}%')

# encode categorical column from data test
encoder, test_set_clean = categorical_encoding(data = test_set_clean,
                                               fit = True)

# split input and output data
X_test, y_test = split_input_output(data = test_set_clean,
                                    target_column = 'price')

# predict data test with best model
y_pred_test = best_regressor.predict(X_test)
test_rmse = root_mean_square_error(y_true = y_test,
                                   y_pred = y_pred_test)

# calculate r2 score
test_r2 = r2_score(y_test, y_pred_test)

print(f'RMSE Test set: {round(test_rmse, 2)}')
print(f'R2 Score Test set: {round(test_r2, 2) * 100}%')

"""##Prediction"""

# create a scatter plot to compare actual and predicted flight fares
sns.scatterplot(x = y_test, y = y_pred_test)
plt.xlabel('Actual Flight Fare')
plt.ylabel('Predicted Flight Fare')
plt.title('Prediction vs Actual Flight Fare')

"""###Feature importance"""

importances = best_regressor.feature_importances_

for feature, importance in zip(X_train.columns, importances):
    print(f'{feature} : {importance}')

feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importances
})

feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
top_features = feature_importance_df.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_features['Feature'], top_features['Importance'], color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Feature Importance from Random Forest')
plt.gca().invert_yaxis()
plt.show()

"""###Partial Dependence Plot"""

from sklearn.inspection import PartialDependenceDisplay

features = X_train.columns.tolist()
num_features = len(features)
fig, ax = plt.subplots(nrows=6, ncols=5, figsize=(18, 14), squeeze=False)
ax = ax.flatten()

for i, feature in enumerate(features):
    PartialDependenceDisplay.from_estimator(best_regressor,
                                            X_train,
                                            [feature],
                                            ax = ax[i],
                                            grid_resolution=50)
    ax[i].set_title(f'{feature}')

plt.tight_layout()
plt.show()

"""###LIME"""

!pip install lime

from lime import lime_tabular

explainer = lime_tabular.LimeTabularExplainer(
    training_data = X_train.values,
    feature_names = X_train.columns,
    mode = 'regression'
)

feature_contributions = []

for i in range(10):
    print(dict(zip(X_train.columns, X_test.iloc[i])))

    explanation = explainer.explain_instance(
        data_row = X_test.iloc[i].values,
        predict_fn = best_regressor.predict,
        num_features = len(X_train.columns)
    )

    contribution_dict = {feat: contrib for feat, contrib in explanation.as_list()}
    feature_contributions.append(contribution_dict)

    fig = explanation.as_pyplot_figure()
    plt.tight_layout()
    plt.show()

contributions_df = pd.DataFrame(feature_contributions).fillna(0)
contributions_df

avg_contributions = contributions_df.mean()
avg_contrib_sort = avg_contributions.sort_values(ascending=False)
avg_contrib_sort

top_10_contrib = avg_contrib_sort.head(10)

plt.figure(figsize=(10, 6))
top_10_contrib.plot(kind='barh', color='skyblue')
plt.xlabel('Average Feature Contribution')
plt.title('Top 10 Feature Contributions to Flight Fare Prediction')
plt.gca().invert_yaxis()
plt.show()

"""###Revenue By days left"""

X_test_simulation = X_test.copy()

days_left_scenarios = range(1, 30)
revenue_days_left = []

for days in days_left_scenarios:
    X_test_simulation['days_left'] = days
    predicted_prices = best_regressor.predict(X_test_simulation)
    total_revenue = np.sum(predicted_prices)
    revenue_days_left.append((days, total_revenue))

revenue_df = pd.DataFrame(revenue_days_left, columns=['Days Left', 'Revenue'])
revenue_df.head(10)

plt.figure(figsize=(10,6))
plt.plot(revenue_df['Days Left'], revenue_df['Revenue'])
plt.xlabel('Days Left')
plt.ylabel('Revenue')
plt.title('Dynamic Pricing Simulation: Revenue by Days Left')
plt.grid(True)
plt.show()

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from textblob import TextBlob  # For sentiment analysis

# Load data
@st.cache
def load_data():
    data = pd.read_csv("Clean_Dataset.csv")
    # Adding simulated ratings and reviews
    data['Ratings'] = np.random.randint(1, 6, size=len(data))  # Ratings: 1 to 5
    data['Reviews'] = np.random.choice(
        ["Great experience", "Average service", "Not worth the price",
         "Excellent value for money", "Poor customer support"], len(data)
    )
    # Simulate additional costs
    data['Baggage_Fee'] = np.random.randint(0, 51, size=len(data))  # $0 - $50
    data['Seat_Selection_Fee'] = np.random.randint(0, 21, size=len(data))  # $0 - $20
    return data

# Categorize flights
def categorize_flights(data):
    data['Departure_Hour'] = pd.to_datetime(data['Departure_Time']).dt.hour
    data['Shift'] = data['Departure_Hour'].apply(lambda x: 'Morning' if 6 <= x < 18 else 'Evening')
    return data

# Dynamic filters
def filter_data(data, airline, shift, departure_city, destination_city, price_range):
    filtered_data = data[
        (data['Airline'] == airline if airline else True) &
        (data['Shift'] == shift if shift else True) &
        (data['Departure_City'] == departure_city if departure_city else True) &
        (data['Destination_City'] == destination_city if destination_city else True) &
        (data['Price'] >= price_range[0]) & (data['Price'] <= price_range[1])
    ]
    return filtered_data

# Sentiment analysis
def sentiment_analysis(reviews):
    sentiments = [TextBlob(review).sentiment.polarity for review in reviews]
    return ["Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral" for sentiment in sentiments]

# Streamlit App
def main():
    st.title("Advanced Flight Price Prediction and Analysis")
    st.sidebar.title("Filters and Options")

    # Load data
    data = load_data()
    data = categorize_flights(data)

    # Sidebar filters
    airlines = st.sidebar.selectbox("Select Airline", options=[None] + list(data['Airline'].unique()))
    shift = st.sidebar.selectbox("Select Flight Shift", options=[None, "Morning", "Evening"])
    departure_city = st.sidebar.selectbox("Select Departure City", options=[None] + list(data['Departure_City'].unique()))
    destination_city = st.sidebar.selectbox("Select Destination City", options=[None] + list(data['Destination_City'].unique()))
    price_range = st.sidebar.slider("Select Price Range", int(data['Price'].min()), int(data['Price'].max()), (int(data['Price'].min()), int(data['Price'].max())))

    # Filter data based on selections
    filtered_data = filter_data(data, airlines, shift, departure_city, destination_city, price_range)
    st.write(f"### Filtered Results ({len(filtered_data)} flights)")
    st.write(filtered_data)

    # Ratings and reviews
    st.header("Airline Ratings and Reviews")
    avg_ratings = filtered_data.groupby('Airline')['Ratings'].mean().sort_values()
    st.bar_chart(avg_ratings)
    filtered_data['Sentiment'] = sentiment_analysis(filtered_data['Reviews'])
    st.write("Sentiments of Reviews:")
    st.write(filtered_data[['Airline', 'Reviews', 'Sentiment']])

    # Additional costs visualization
    st.header("Additional Costs Breakdown")
    additional_costs = filtered_data[['Airline', 'Baggage_Fee', 'Seat_Selection_Fee']].groupby('Airline').mean()
    st.bar_chart(additional_costs)

    # Personalized recommendations
    st.header("Personalized Recommendations")
    cheapest_flight = filtered_data.loc[filtered_data['Price'].idxmin()] if not filtered_data.empty else None
    if cheapest_flight is not None:
        st.subheader("Cheapest Flight")
        st.write(f"**Airline**: {cheapest_flight['Airline']}")
        st.write(f"**Price**: ${cheapest_flight['Price']}")
        st.write(f"**Shift**: {cheapest_flight['Shift']}")
        st.write(f"**Departure City**: {cheapest_flight['Departure_City']}")
        st.write(f"**Destination City**: {cheapest_flight['Destination_City']}")
    else:
        st.write("No flights available with the current filters.")

    # Seasonal insights
    st.header("Seasonal Insights")
    seasonal_data = data.copy()
    seasonal_data['Month'] = pd.to_datetime(seasonal_data['Departure_Date']).dt.month
    avg_monthly_price = seasonal_data.groupby('Month')['Price'].mean()
    st.line_chart(avg_monthly_price)

if __name__ == "__main__":
    main()
