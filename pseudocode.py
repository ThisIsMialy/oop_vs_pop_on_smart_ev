BEGIN SmartCampusEVSystem
  // does not change during program being run
  CONSTANT TYPE charger_rates AS DICTIONARY
  TYPE charger_rates = { 
    1 : {
      Name : "AC Fast Charger"
      Rate : [4.00, 6.00, 8.00, 12.00] // tier 0,1,2,3
      Maximum : 80.00
    }, 
    2 : {
      Name : "DC Fast Charger"
      Rate : [10.00, 15.00, 20.00, 30.00]  // tier 0,1,2,3
      Maximum : 150.00
    }, 
  }

  CONSTANT TYPE discounts AS DICTIONARY
  TYPE discounts = {
    1 : {
      Name: "First-Time User (New Registration)",
    },
    2 : {
      Name: "Staff Discount",
    },
    3 : {
      Name : "Student Discount (AC Charger Only)",
    },
    4 : {
      Name: "Green Eco-Pass Holder (Certified EV)",
    }
  }
  
  CONSTANT TYPE surcharges AS DICTIONARY
  TYPE surcharges = {
    1 : {
      Name: "Peak Hour Charging Surcharge (12 PM - 4 PM)",
      Amount : 5.00
    },
    2 : {
      Name: "Idle Parking Surcharge",
      Amount : 15.00
    },
    3 : {
      Name: "Lost RFID Access Card Replaceemnt Fee",
      Amount : 30.00
    }
  }
  
  // Loop Entire Program
  WHILE TRUE: 
    // Assume: Userid and vehicle numbers can have alphanumerical characters
    // Assume: Only students and staff are allowed to use EV charging
    DECLARE user_id, vehicle_number AS STRING
    DECLARE member_type AS INTEGER // User will choose
    DECLARE charger_type AS CHAR
    DECLARE session_duration AS FLOAT
    
    // DISCOUNT CONDITIONS
    DECLARE new_user, certified_ev AS BOOLEAN
    // SURCHARGE CONDITIONS
    DECLARE peak_hour, idle_parking, card_replacement AS BOOLEAN
    
    // BILL 
    DECLARE gross_fee =  0 AS FLOAT
    DECLARE discount_total = 0 AS FLOAT
    DECLARE surcharge_total = 0 AS FLOAT
    DECLARE net_payable = 0 AS FLOAT
    
    INPUT user_id, vehicle_number, session_duration
    session_duration = ROUND UP (session_duration)
    OUTPUT ("1 FOR STAFF, 2 FOR STUDENT: ")
    INPUT member_type // TRY CATCH HERE if not 1 or 2
    OUTPUT ("1 FOR AC FAST CHARGER, 2 FOR DC: ")
    INPUT charger_type // TRY CATCH HERE if not 1 or 2
  
    INPUT new_user, certified_ev
    INPUT peak_hour, idle_parking, card_replacement
    
    FUNCTION ChargedTier(session_duration)
      DECLARE tier = 0 AS INTEGER
      IF session_duration < 3 THEN tier = 0
      ELSE IF session_duration < 5 THEN tier = 1
      ELSE IF session_duration < 7 THEN tier = 2
      ELSE IF session_duration > 6 THEN tier = 3
      ENDIF
      RETURN tier AS INTEGER
    ENDFUNCTION
  
    
    // first function that gets called
    FUNCTION GrossFee()
      this_tier = CALL ChargedTier(session_duration)
      // get the rate for this tier for this charger type from DICTIONARY
      this_rate = charger_rates.[index=charger_type].Rate[index=this_tier]
      maximum = charger_rates.[index=charger_type].Maximum
      gross_fee = session_duration * this_rate
      IF gross_fee > maximum THEN
        RETURN maximum 
      ELSE THEN RETURN gross_fee
    ENDFUNCTION
    
    FUNCTION ApplyDiscount(gross_fee)
      DECLARE this_discount = 0 AS FLOAT
      // immediately stop if new user, do not apply further discount
      IF new_user THEN RETURN gross_fee
      ENDIF
      
      IF member_type == 1 THEN this_discount += gross_fee * 0.5
      ELSE IF member_type == 2 AND charger_type == 1 THEN 
        this_discount += gross_fee * 0.25
      ENDIF
      
      IF certified_ev THEN this_discount += 2.00
      ENDIF 
      
      RETURN this_discount
    ENDFUNCTION
    
    FUNCTION ApplySurcharge()
      DECLARE this_surcharge = 0 AS FLOAT
      IF peak_hour THEN this_surcharge += surcharges[key=1].Amount
      ENDIF
      IF idle_parking THEN this_surcharge += surcharges[key=2].Amount
      ENDIF
      IF card_replacement THEN this_surcharge += surcharges[key=3].Amount
      ENDIF
      
      RETURN this_surcharge
    ENDFUNCTION
    
    FUNCTION NetPayable(gross, discount, surcharge)
      this_payable = gross + surcharge - discount
      RETURN this_payable
    ENDFUNCTION
 
    PROCEDURE BillOutput()
      gross_fee = CALL GrossFee()
      discount_total = CALL ApplyDiscount(gross_fee)
      surcharge_total = CALL ApplySurcharge()
      net_payable = CALL NetPayable(gross_fee, discount_total, surcharge_total
      
      OUTPUT "GROSS FEE: RM ", gross_fee
      OUTPUT "DISCOUNT: RM ", discount_total
      OUTPUT "SURCHARGES: RM ", surcharge_total
      OUTPUT "NET PAYABLE: RM ", net_payable
    ENDPROCEDURE
    
    CALL BillOutput()
    
    OUTPUT "EXIT?"
    DECLARE exit_program AS BOOLEAN
    INPUT exit_program
    IF exit_program: 
      THEN BREAK // FORCE EXIT
    ENDIF  
  
  ENDWHILE
  
END SmartCampusEVSystem
